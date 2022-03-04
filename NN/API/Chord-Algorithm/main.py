#internal
import functions as func
import hmm
import match_templates as temp
import chordACA
import librosa
import soundfile as sf
from pydub.utils import mediainfo
import matplotlib.pyplot as plt
import numpy as np
import dictionary as dict


# temp
import libfmp.b
import libfmp.c3
import libfmp.c4
import os



# Testing with temp files
def main():
    path = "../Data/Audio/N8BXtM6onEY.wav"
    
    # Used for debug/testing sample rate
    #y, sr = librosa.load(path)
    #path = "../Data/Audio/test.wav"
    #sf.write(path, y, sr)
    #timeframe = (29, 39)
    
    #func.songHandler(path)               # Check with handling the different algorithms 
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
    
    margin_i, margin_v = 2, 10
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
    S_fore = np.abs(S_foreground)**2          # try non-stft versions
    fore = librosa.feature.chroma_stft(S=S_fore, sr=sr)
    
    S_back = np.abs(S_background)**2          # try non-stft versions
    back = librosa.feature.chroma_stft(S=S_back, sr=sr)

    fig, ax = plt.subplots()
    plt.xlim(29, 39)
    img = librosa.display.specshow(fore, y_axis='chroma', x_axis='time', ax=ax)
    ax.set(title='Foreground mask')
    fig.colorbar(img, ax=ax)
    plt.show()
    
    
    fig, ax = plt.subplots()
    plt.xlim(29, 39)
    img = librosa.display.specshow(back, y_axis='chroma', x_axis='time', ax=ax)
    ax.set(title='Background mask')
    fig.colorbar(img, ax=ax)
    plt.show()
    
if __name__ == "__main__":
    main()
