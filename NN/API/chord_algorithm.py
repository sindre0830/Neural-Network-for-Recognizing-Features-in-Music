# import local modules
import dictionary as dict
# import foreign modules
import pyACA
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import preprocessing
import keras


# Object to perform chord tracking.
class ChordRecognizer:
    id: str
    chords: np.ndarray

    # Construct ChordRecognizer object.
    def __init__(self, id: str):
        self.id = id

    # Compute chord recognizer.
    def run(self, beats: np.ndarray, model: keras.models.Sequential, solution: str = "CNN", plot: bool = False, verbose: bool = False):
        # preprocess
        dict.printOperation("Preprocess data...", verbose=verbose)
        preprocessing.splitAudio(self.id, mode=dict.STEMS2, output=dict.ACCOMPANIMENT)
        preprocessing.resampleAudio(self.id, dict.SAMPLERATE_CHORDS)
        dict.printMessage(dict.DONE, verbose=verbose)
        # get results
        dict.printOperation("Running chord tracker...", verbose=verbose)
        if solution == "CNN":
            self.runModel(beats, model)
        elif solution == "ALG":
            self.getChords(beats)
        dict.printMessage(dict.DONE, verbose=verbose)
        # plot
        if plot:
            dict.printOperation("Plotting results...", verbose=verbose)
            self.plot(start=beats[2], end=beats[3])
            dict.printMessage(dict.DONE, verbose=verbose)
        dict.printDivider(verbose=verbose)

    # Runs the neural network model.
    def runModel(self, beats: np.ndarray, model: keras.models.Sequential):
        chords = []
        lastDuration = 0.
        for i in range(beats.shape[0]):
            # get audio sample between two beats and generate chromagram
            if i + 1 < len(beats):
                end = beats[i + 1]
                start = beats[i]
                duration = (end - start)
                lastDuration = duration
            else:
                duration = lastDuration
            y, sr = librosa.load(dict.getModifiedAudioPath(self.id), sr=None, offset=start, duration=duration)
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            # resize matrix to uniform length
            # max_length is decided by the data gathering in preprocessing.getTrainingData() in will have to be updated for each time it is run
            mat = preprocessing.extendMatrix(mat=chroma, max_length=47)
            mat = np.expand_dims(mat, axis=0)
            # get predictions and append the label with highest score
            predictions = model.predict(mat)
            index = np.argmax(predictions)
            chords.append(dict.chords[index])
        self.chords = np.array(chords)

    # Gets chords from audio file.
    def getChords(self, beats: np.ndarray):
        chords = []
        for i in range(beats.shape[0]):
            end = None
            if i + 1 < len(beats):
                end = beats[i + 1]
            chords.append(self.getChord(start=beats[i], end=end))
        self.chords = np.array(chords)

    # Gets chord between beat.
    def getChord(self, start: float, end: float = None):
        duration = None
        if end is not None:
            duration = (end - start)
        y, sr = librosa.load(dict.getModifiedAudioPath(self.id), sr=None, offset=start, duration=duration)
        (_, arrIndex, _, _) = pyACA.computeChords(y, sr)
        chordIndex = np.bincount(arrIndex[0]).argmax()
        chord = dict.chords[chordIndex]
        return np.array(chord)

    # Plots the chromagram.
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
