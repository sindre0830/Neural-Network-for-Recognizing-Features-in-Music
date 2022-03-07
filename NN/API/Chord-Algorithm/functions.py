# external
import libfmp.c4
import libfmp.c3
import libfmp.b
import os
import sys
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
from pydub.utils import mediainfo
from pydub import AudioSegment
from math import floor
from statistics import mode
from pathlib import Path, PurePosixPath
import soundfile as sf

# internal
import dictionary as dict
import chordACA
import hmm
import match_templates as temp


# handles running various chord recognition algorithms
def songHandler(path, timeframe=None):
    # Chroma
    #getChromagram(path, timeframe)
    # Chords
    chordACA.getChords(path, timeframe)
    #hmm.getMarkovChords(path, timeframe)
    # temp.templateMatch(path, timeframe)        # Seems really bad


# Loads with librosa
# If we want to split and use those for  NN training, we might have to manually keep
# track of the splits by passing in individually and storing in arrays...
def getLibRosaChords(path):
    data, sample = librosa.load(path, sr=int(mediainfo(path)['sample_rate']))
    # Not sure we want floor?
    plotChromaSlices(data, sample, floor(float(mediainfo(path)['duration'])))


# plots chromagram
def getChromagram(path, timeframe=None):
    y, sr = librosa.load(path)

    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    fig, ax = plt.subplots()
    img = librosa.display.specshow(
        chroma, y_axis='chroma', x_axis='time', ax=ax)
    ax.set(title='Chromagram demonstration')
    fig.colorbar(img, ax=ax)
    if timeframe is not None:
        plt.xlim(timeframe)    # set timeframe
    plt.show()


# Performs plotting
# Rather than plot, we want to just get the data out
def plotChromaSlices(data, sample, duration):
    librosa.feature.chroma_stft(y=data, sr=sample)

    # Energy spectrogram
    #S = np.abs(librosa.stft(data))

    # Power spectrogram
    S = np.abs(librosa.stft(data, n_fft=4096))**2

    # get number of windows and set hop size relative to window size (cover half of window each time)
    windows = duration // dict.win_s
    hop = windows * 2

    # We split our spectrogram data into windows
    sources = splitSong(S, duration)

    # Elegant way to get rid of extra nesting?
    for source in sources[0]:
        chroma = librosa.feature.chroma_stft(S=source, sr=sample)
        # Also consider trying CQT chromagram
        # chroma = librosa.feature.chroma_cqt(S=source, sr=sample)

        # This is where we want to be instead analyzing the data and getting
        # the chord from the pitches
        plotSong(chroma, source)
        # pitches = []
        # dominant_pitch = ""

        # new_chroma = np.swapaxes(chroma,0,1)
        # for pitch in new_chroma:
        #     oneD = pitch.flatten()
        #     pitches.append(getPitch(oneD))      # We want to get Chords instead

        # # Basic handling of pitches - currently either prints each frame,
        # # or prints the dominant pitch (if any) for the section (6 seconds windows)
        # most_frequent = mode(pitches)
        # if pitches.count(most_frequent) / len(pitches) > 0.3:
        #     dominant_pitch = most_frequent
        #     print("The dominant pitch is: " + dominant_pitch)
        # else:
        #     print("No dominant pitch found for this part.")


# Splits song into small windows
# Function assumes 2d numpy array where y-axis represents time
def splitSong(path, duration):
    windows = duration // dict.win_s
    hop = windows * 2

    # We use sliding_window_view to get windows, set the size of each window with the variables above,
    # and use slicing with our hop size so we do not get a window for every frame
    return np.lib.stride_tricks.sliding_window_view(
        path,
        window_shape=(np.shape(path)[0], np.shape(path)[1]//windows))[:, ::np.shape(path)[1]//hop]


# Plots the song as a diagram - mostly used for debugging/testing
def plotSong(chroma, source):
    fig, ax = plt.subplots(nrows=2, sharex=True)
    img = librosa.display.specshow(librosa.amplitude_to_db(
        source, ref=np.max), y_axis='log', x_axis='time', ax=ax[0])
    fig.colorbar(img, ax=[ax[0]])
    ax[0].label_outer()
    img = librosa.display.specshow(
        chroma, y_axis='chroma', x_axis='time', ax=ax[1])
    fig.colorbar(img, ax=[ax[1]])


# Defines the dominant pitch of one frame from the pitch values
def getPitch(pitch):
    max_value = np.max(pitch)
    max_index = np.where(pitch == max_value)
    return dict.pitches[max_index[0][0]]


# To be implemented
# def getChord(pitch):

def splitSong(path):
    info = mediainfo(path)
    d = floor(float(info["duration"]))
    slices = d // dict.win_s
    m = 1000

    for slice in range(slices):
        newAudio = AudioSegment.from_wav(path)
        newAudio = newAudio[dict.win_s*slice*m: (dict.win_s*(slice+1)*m) - 1]
        newAudio.export(dict.BASE_DIR + dict.SLICE_DIR +
                        PurePosixPath(path).stem + str(slice)+".wav", format="wav")
    print("Song " + PurePosixPath(path).stem +
          " successfully split into " + str(slices) + " slices.")


def librosaVocalFilter(path):
# Compute chroma features
    fn_wav = path
    N = 4096
    H = 2048
    y, sr = librosa.load(fn_wav)
    
    S_full, phase = librosa.magphase(librosa.stft(y))
    
    S_filter = librosa.decompose.nn_filter(S_full,
                                       aggregate=np.median,
                                       metric='cosine',
                                       width=int(librosa.time_to_frames(2, sr=sr)))
    S_filter = np.minimum(S_full, S_filter)
    
    margin_i, margin_v = 2,10
    power = 2

    mask_i = librosa.util.softmask(S_filter,
                                margin_i * (S_full - S_filter),
                                power=power)

    mask_v = librosa.util.softmask(S_full - S_filter,
                                margin_v * S_filter,
                                power=power)

    # Once we have the masks, simply multiply them with the input spectrum
    # to separate the components

    S_foreground = mask_v * S_full
    S_background = mask_i * S_full

    # not great results...must look at
    S_fore = np.abs(S_foreground)**2
    S_back = np.abs(S_background)**2

    fore = librosa.feature.chroma_stft(S=S_fore, sr=sr, n_chroma=12, n_fft=4096)
    #print(np.shape(fore))
    
    back = librosa.feature.chroma_stft(S=S_back, sr=sr)
    
    orig = librosa.feature.chroma_stft(S=S_full, sr=sr)

    # cqt - doesn't work because of shape...    
    # fore = librosa.feature.chroma_cqt(y=S_fore, sr=sr)
    # print(np.shape(fore))

    # back = librosa.feature.chroma_cqt(y=S_back, sr=sr)
    
    # orig = librosa.feature.chroma_cqt(y=S_full, sr=sr)


    fig, ax = plt.subplots()
    plt.xlim(29, 34)
    img = librosa.display.specshow(orig, y_axis='chroma', x_axis='time', ax=ax)
    ax.set(title='Original')
    fig.colorbar(img, ax=ax)
    plt.show()


    fig, ax = plt.subplots()
    plt.xlim(29, 34)
    img = librosa.display.specshow(fore, y_axis='chroma', x_axis='time', ax=ax)
    ax.set(title='Foreground mask')
    fig.colorbar(img, ax=ax)
    plt.show()
    
    
    fig, ax = plt.subplots()
    plt.xlim(29, 34)
    img = librosa.display.specshow(back, y_axis='chroma', x_axis='time', ax=ax)
    ax.set(title='Background mask')
    fig.colorbar(img, ax=ax)
    plt.show()
    
    # not actually doing a good job
    new_y = librosa.istft(S_background*phase)
    sf.write("../Data/background.wav", new_y, sr)
