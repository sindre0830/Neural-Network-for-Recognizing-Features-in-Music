# import local modules
import dictionary as dict
# import foreign modules
import pyACA
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import preprocessing


# Object to perform chord tracking.
class ChordRecognizer:
    id: str
    chords: np.ndarray

    # Construct ChordRecognizer object.
    def __init__(self, id: str):
        self.id = id

    # Compute chord recognizer.
    def run(self, beats: np.ndarray, plot: bool = False, verbose: bool = False):
        # preprocess
        dict.printOperation("Preprocess data...", verbose=verbose)
        preprocessing.splitAudio(self.id, mode=dict.STEMS2, output=dict.ACCOMPANIMENT)
        preprocessing.resampleAudio(self.id, dict.SAMPLERATE_CHORDS)
        dict.printMessage(dict.DONE, verbose=verbose)
        # get results
        dict.printOperation("Running chord tracker...", verbose=verbose)
        self.getChords(beats)
        dict.printMessage(dict.DONE, verbose=verbose)
        # plot
        if plot:
            dict.printOperation("Plotting results...", verbose=verbose)
            self.plot(start=beats[2], end=beats[3])
            dict.printMessage(dict.DONE, verbose=verbose)
        dict.printDivider(verbose=verbose)

    def getChords(self, beats: np.ndarray):
        chords = []
        for i in range(beats.shape[0]):
            end = None
            if i + 1 < len(beats):
                end = beats[i+1]
            chords.append(self.getChord(start=beats[i], end=end))
        self.chords = np.array(chords)

    # Gets chord between beat
    def getChord(self, start: float, end: float = None):
        duration = None
        if end is not None:
            duration = (end - start)
        y, sr = librosa.load(dict.getModifiedAudioPath(self.id), sr=None, offset=start, duration=duration)
        (label, _, _, _) = pyACA.computeChords(y, sr)
        chord = self.pickChord(label[0])
        return np.array(chord)

    # Plots the chromagram
    def plot(self, start: float = None, end: float = None):
        y, sr = librosa.load(dict.getModifiedAudioPath(self.id), sr=None)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        librosa.display.specshow(chroma, x_axis='time', y_axis='chroma')
        # trim figure between two timestamps
        if start is not None:
            plt.xlim(left=start)
        if end is not None:
            plt.xlim(right=end)
        plt.show()

    def pickChord(self, labels):
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