# import local modules
import dictionary as dict
# import foreign modules
import pyACA
import matplotlib.pyplot as plt
import librosa
import librosa.display


def chordHandler(id, beats, verbose=False):
    chords = []
    for i in range(len(beats)-1):
        chords += [getChord(id, beats[i], beats[i+1])]
    if verbose:
        pass    # Plot here, TBD
    return chords
        

# gets chords between timestamps
def getChord(id: str, start: float, end: float):
    y, sr = librosa.load(dict.getModifiedAudioPath(id), sr=None, offset=start, duration=(end - start))
    (label, _, _, _) = pyACA.computeChords(y, sr)
    return pickChord(label[0])


def pickChord(labels):
    chords = {}
    counter = len(labels)       # Weighting
    for chord in labels:
        if not chord in chords:
            chords[chord] = 1
        else:
            chords[chord] += 1
        chords[chord] += (counter / len(labels)) # Add weighting, prioritizing early #s
        counter -= 1
    mode = [i for i in set(labels) if labels.count(i) == max(map(labels.count, labels))]
    # If one most common chord, return it
    if len(mode) == 1:
        return mode[0]
    # If multiple most common, use weighting
    else:
        s = max(chords, key=chords.get)
        return s
    


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
