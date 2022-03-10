# external
import pyACA
import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display

#internal
import dictionary as dict


# get chroma with chordACA
def chordACA(id, timeframe=None):
    #(label, index, time, P_E) = pyACA.computeChordsCl(dict.getModifiedAudioPath(id))
    y, sr = librosa.load(dict.getModifiedAudioPath(id), sr=None)
    (label, index, time, P_E) = pyACA.computeChords(y, sr)
    plt.title("Identified chords - pyACA")
    if timeframe is not None:
        plt.xlim(timeframe)
    plt.scatter(time, label[0])
    plt.show()


# Plots the song as a chromagram - mostly used for debugging/testing
def plotChromagram(id):
    y, sr = librosa.load(dict.getModifiedAudioPath(id), sr=None)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    plt.figure(figsize=(15, 5))
    librosa.display.specshow(chroma, x_axis='time', y_axis='chroma')
    plt.show()
