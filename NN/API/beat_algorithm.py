# import local modules
import dictionary as dict
import preprocessing
# import foreign modules
import matplotlib.pyplot as plt
import librosa
import librosa.display
import librosa.beat
import os
import numpy as np
import json


# Object to perform beat tracking.
class BeatRecognizer:
    id: str
    beats: np.ndarray
    bpm: float

    # Construct BeatRecognizer object.
    def __init__(self, id: str):
        self.id = id

    # Compute beat recognizer.
    def run(self, plot: bool = False, plot_start: float = None, plot_end: float = None, verbose: bool = False):
        # preprocess
        dict.printOperation("Preprocess data...", verbose=verbose)
        preprocessing.splitAudio(self.id, mode=dict.NO_STEMS)
        preprocessing.resampleAudio(self.id, dict.SAMPLERATE_BEATS)
        dict.printMessage(dict.DONE, verbose=verbose)
        # get results
        dict.printOperation("Running beat tracker...", verbose=verbose)
        self.librosaBeatAnalysis()
        dict.printMessage(dict.DONE, verbose=verbose)
        # plot
        if plot:
            dict.printOperation("Plotting results...", verbose=verbose)
            self.plot(start=plot_start, end=plot_end)
            dict.printMessage(dict.DONE, verbose=verbose)
        # clean-up
        dict.printOperation("Cleaning up...", verbose=verbose)
        preprocessing.deleteAudioFile(dict.getModifiedAudioPath(self.id))
        dict.printMessage(dict.DONE, verbose=verbose)
        dict.printDivider(verbose=verbose)

    # Get beats and BPM from Librosa's beat tracker.
    def librosaBeatAnalysis(self):
        # loads audio file and gets bpm and beat timestamps
        y, sr = librosa.load(dict.getModifiedAudioPath(self.id), sr=None)
        self.bpm, self.beats = librosa.beat.beat_track(y=y, sr=sr, units="time")

    # Plots beat timestamps.
    def plot(self, start=None, end=None):
        # load audio file
        y, sr = librosa.load(dict.getModifiedAudioPath(self.id), sr=None)
        # plot onset strength
        onset_env = librosa.onset.onset_strength(y=y, sr=sr, aggregate=np.median)
        times = librosa.times_like(onset_env, sr=sr, hop_length=512)
        plt.plot(times, librosa.util.normalize(onset_env), alpha=0.6)
        plt.xlabel("Time")
        plt.ylabel("Onset strength")
        # plot beat timestamps
        n = 1
        # branch if database has been loaded
        if dict.FLAG_DATABASE:
            plt.vlines(self.beats, 0.5, 1, color="g", linestyle="--", label="Librosa")
            # read json file and plot data from database
            with open(dict.PROCESSED_JSON_PATH, 'r') as f:
                document = json.loads(f.read())
            plt.vlines(document[self.id]["beats"], 0, 0.5, color="black", linestyle="--", label="Manual")
            n = 2
        else:
            plt.vlines(self.beats, 0, 1, color="g", linestyle="--", label="Librosa")
        # set other parameters
        plt.ylim(0, 1)
        plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left", mode="expand", ncol=n)
        plt.title(self.id + "  -  " + str(sr) + " sample rate", pad=40.)
        plt.xlabel("Time")
        plt.ylabel("Onset strength")
        # trim figure between two timestamps
        if start is not None:
            plt.xlim(left=start)
        if end is not None:
            plt.xlim(right=end)
        # branch if plot directory doesn't exist
        if not os.path.exists(dict.PLOTS_PATH):
            os.makedirs(dict.PLOTS_PATH)
        # save plot as PNG and show results
        plt.subplots_adjust(top=0.8)
        plt.savefig(dict.getPlotPath(self.id), dpi=300, transparent=True, bbox_inches="tight")
        plt.show()
