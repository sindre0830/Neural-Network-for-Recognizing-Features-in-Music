# external
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
from pydub.utils import mediainfo
from math import floor
from statistics import mode

# internal
import dictionary as dict

# Loads with librosa
# If we want to split and use those for  NN training, we might have to manually keep
# track of the splits by passing in individually and storing in arrays...
def songHandler(path):
    data, sample = librosa.load(path, sr = int(mediainfo(path)['sample_rate']))
    plotChroma(data, sample, floor(float(mediainfo(path)['duration'])))        # Not sure we want floor?
    
    
# Performs plotting
# Rather than plot, we want to just get the data out
def plotChroma(data, sample, duration):
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
        #plotSong(chroma, source)
        pitches = []
        dominant_pitch = ""

        new_chroma = np.swapaxes(chroma,0,1)
        for pitch in new_chroma:
            oneD = pitch.flatten()
            pitches.append(getChord(oneD))
        
        # Basic handling of pitches - currently either prints each frame,
        # or prints the dominant pitch (if any) for the section (6 seconds windows)
        most_frequent = mode(pitches)
        if pitches.count(most_frequent) / len(pitches) > 0.3:
            dominant_pitch = most_frequent
            print("The dominant pitch is: " + dominant_pitch)
        else:
            print("No dominant pitch found for this part.")
            
    
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
    img = librosa.display.specshow(librosa.amplitude_to_db(source,ref=np.max), y_axis='log', x_axis='time', ax=ax[0])
    fig.colorbar(img, ax=[ax[0]])
    ax[0].label_outer()
    img = librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax[1])
    fig.colorbar(img, ax=[ax[1]])


# Defines the chord of one frame from the pitch values
def getChord(pitch):
    max_value = np.max(pitch)
    max_index = np.where(pitch == max_value)
    return dict.pitches[max_index[0][0]]
