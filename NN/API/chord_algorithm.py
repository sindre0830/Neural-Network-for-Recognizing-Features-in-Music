#external
import pyACA
import matplotlib.pyplot as plt 
import numpy as np
import os 
import librosa

#internal
import dictionary as dict


# get chroma with chordACA
def chordACA(path, timeframe):
    
    (label, index, time, P_E) = pyACA.computeChordsCl(path)
    
    plt.title("Identified chords - pyACA")
    plt.xlim(timeframe)                   # only 50 - 60 sec
    plt.scatter(time, label[0])        # Believe this is correct one but not sure
    plt.show()
    
    
# get chroma with librosa
def chordLibrosa(path, timeframe=None):
    y, sr = librosa.load(path)

    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    
    plotChord(chroma, y, timeframe)
    
    
# Plots the song as a diagram - mostly used for debugging/testing
def plotChord(chroma, source, timeframe=None):
    fig, ax = plt.subplots(nrows=2, sharex=True)
    img = librosa.display.specshow(librosa.amplitude_to_db(
        source, ref=np.max), y_axis='log', x_axis='time', ax=ax[0])
    if timeframe is not None:
        plt.xlim(timeframe)    # set timeframe
    fig.colorbar(img, ax=[ax[0]])
    ax[0].label_outer()
    img = librosa.display.specshow(
        chroma, y_axis='chroma', x_axis='time', ax=ax[1])
    fig.colorbar(img, ax=[ax[1]])


