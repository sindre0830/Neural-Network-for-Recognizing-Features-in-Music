# import local modules
import dictionary as dict
# import foreign modules
import matplotlib.pyplot as plt
import librosa
import librosa.display
import librosa.beat
import os


# Get beats and BPM from Librosa's beat tracker.
def librosaBeatAnalysis(id):
    # loads audio file and gets bpm and beat timestamps
    y, sr = librosa.load(dict.getModifiedAudioPath(id), sr=None)
    return librosa.beat.beat_track(y=y, sr=sr, units="time")


# Plots beat timestamps.
def plotBeats(id, manual_beats=None, aubio_beats=None, librosa_beats=None, start=None, end=None):
    # load audio file
    y, sr = librosa.load(dict.getModifiedAudioPath(id), sr=None)
    # plot waveform and add title
    librosa.display.waveplot(y, alpha=0.6)
    plt.title(id + "  -  " + str(sr) + " samplerate", pad=40.)
    # plot beat timestamps
    n = 0
    if aubio_beats is not None:
        plt.vlines(aubio_beats, 0.33, 1, color="r", linestyle="--", label="Aubio")
        n += 1
    if manual_beats is not None:
        plt.vlines(manual_beats, -0.33, 0.33, color="black", linestyle="--", label="Manual")
        n += 1
    if librosa_beats is not None:
        plt.vlines(librosa_beats, -1, -0.33, color="g", linestyle="--", label="Librosa")
        n += 1
    plt.ylim(-1, 1)
    if manual_beats is not None or aubio_beats is not None or librosa_beats is not None:
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
    plt.savefig(dict.getPlotPath(id), dpi=300, transparent=True, bbox_inches="tight")
    plt.show()
