# import local modules
import dictionary as dict
# import foreign modules
import pyACA
import matplotlib.pyplot as plt
import librosa
import librosa.display


# gets chords between timestamps
def getChord(id: str, start: float, end: float):
    y, sr = librosa.load(dict.getModifiedAudioPath(id), sr=None, offset=start, duration=(end - start))
    (label, _, _, _) = pyACA.computeChords(y, sr)
    print(label[0])


# get chroma with chordACA
def chordACA(id, timeframe=None):
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
