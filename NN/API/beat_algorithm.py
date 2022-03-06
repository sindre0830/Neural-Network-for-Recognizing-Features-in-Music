# import local modules
import dictionary as dict
# import foreign modules
import pydub.utils
import aubio
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import librosa.beat
import os


# Get beats and BPM from Librosa's beat tracker.
def librosaBeatAnalysis(path):
    # loads audio file and gets bpm and beat timestamps
    y, sr = librosa.load(path, sr=None)
    return librosa.beat.beat_track(y=y, sr=sr, units="time")


# Handler for aubio analysis.
def aubioBeatAnalysis(path):
    # read metadata of audio file to get the samplerate
    info = pydub.utils.mediainfo(path)
    # gets timestamps and bpm
    beats = extractBeats(path, samplerate=int(info['sample_rate']))
    bpm = getBPM(beats)
    return bpm, beats


# Calculate beats per minute.
def getBPM(beats):
    # if enough beats are found, convert to periods then to bpm
    if len(beats) > 1:
        return np.median(60. / np.diff(beats))
    else:
        return None


# Get timestamps for each beat extracted.
# Source: https://github.com/aubio/aubio/blob/master/python/demos/demo_bpm_extract.py
def extractBeats(path, samplerate, win_s=512, hop_s=256):
    # load file and get tempo
    src = aubio.source(path, samplerate, hop_s)
    o = aubio.tempo("specdiff", win_s, hop_s, src.samplerate)
    # read through the frames and save the timestamp of each found beat
    beats = []
    total_frames = 0
    while True:
        samples, read = src()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
        total_frames += read
        if read < hop_s:
            break
    return beats


# Plots beat timestamps.
def plotBeats(path, manual_beats=None, aubio_beats=None, librosa_beats=None, start=None, end=None):
    # load audio file
    y, _ = librosa.load(path)
    # plot waveform
    librosa.display.waveshow(y, alpha=0.6)
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
    plt.savefig("Data/Plots/tmp.png", dpi=300, transparent=True, bbox_inches="tight")
    plt.show()
