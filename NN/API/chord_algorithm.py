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
    def run(self, beats: np.ndarray, verbose: bool = False):
        # preprocess
        dict.printOperation("Preprocess data...", verbose=verbose)
        preprocessing.splitAudio(self.id, mode=dict.STEMS2, output=dict.ACCOMPANIMENT)
        preprocessing.resampleAudio(self.id, dict.SAMPLERATE_CHORDS)
        dict.printMessage(dict.DONE, verbose=verbose)
        # get results
        dict.printOperation("Running chord tracker...", verbose=verbose)
        self.chords = self.getChord(beats[2], beats[3])

        dict.printMessage(dict.DONE, verbose=verbose)
        # plot
        if verbose:
            dict.printOperation("Plotting results...", verbose=verbose)
            self.plot(start=beats[2], end=beats[3])
            dict.printMessage(dict.DONE, verbose=verbose)
        dict.printDivider(verbose=verbose)

    # gets chords between timestamps
    def getChord(self, start: float, end: float):
        y, sr = librosa.load(dict.getModifiedAudioPath(self.id), sr=None, offset=start, duration=(end - start))
        (label, _, _, _) = pyACA.computeChords(y, sr)
        return np.array(label[0])

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
