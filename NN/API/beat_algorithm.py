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
    def run(self, verbose: bool = False):
        # preprocess
        preprocessing.splitAudio(self.id, mode=dict.NO_STEMS)
        preprocessing.resampleAudio(self.id, dict.SAMPLERATE_BEATS)
        # get results
        self.librosaBeatAnalysis()
        # plot
        if verbose:
            self.plot(start=None, end=None)


    # Get beats and BPM from Librosa's beat tracker.
    def librosaBeatAnalysis(self):
        # loads audio file and gets bpm and beat timestamps
        y, sr = librosa.load(dict.getModifiedAudioPath(self.id), sr=None)
        self.bpm, self.beats = librosa.beat.beat_track(y=y, sr=sr, units="time")


    # Plots beat timestamps.
    def plot(self, start=None, end=None):
        # load audio file
        y, sr = librosa.load(dict.getModifiedAudioPath(self.id), sr=None)
        # plot waveform and add title
        librosa.display.waveplot(y, alpha=0.6)
        plt.title(self.id + "  -  " + str(sr) + " samplerate", pad=40.)
        # plot beat timestamps
        n = 1
        # branch if database has been loaded
        if dict.FLAG_DATABASE:
            # open json file
            with open(dict.PROCESSED_JSON_PATH, 'r') as f:
                document = json.loads(f.read())
            plt.vlines(document[self.id]["beats"], 0, 1, color="black", linestyle="--", label="Manual")
            plt.vlines(self.beats, -1, 0, color="g", linestyle="--", label="Librosa")
            n = 2
        else:
            plt.vlines(self.beats, -1, 1, color="g", linestyle="--", label="Librosa")
        plt.ylim(-1, 1)
        plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left", mode="expand", ncol=n)
        # trim figure between two timestamps
        if start is not None:
            plt.xlim(left=start)
        if end is not None:
            plt.xlim(right=end)
        # branch if plot directory doesn't exist
        if not os.path.exists(dict.PLOTS_DIR):
            os.makedirs(dict.PLOTS_DIR)
        # save plot as PNG and show results
        plt.subplots_adjust(top=0.8)
        plt.savefig(dict.getPlotPath(self.id), dpi=300, transparent=True, bbox_inches="tight")
        plt.show()
