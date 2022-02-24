# import foreign modules
import pydub.utils
import aubio
import numpy as np


# Handler for aubio analysis.
def analyseBeats(path):
    info = pydub.utils.mediainfo(path)
    # gets timestamps and bpm - use arguments if only one is wanted
    (beats, bpm) = get_file_bpm(path, samplerate=int(info['sample_rate']))
    # decide what to do with output here - currently just prints
    print(path)
    if bpm is not None:
        print(bpm)
    if beats is not None:
        print(beats)   
    print(info['sample_rate'])


# Improve error handling here
def beats_to_bpm(beats, path):
    # if enough beats are found, convert to periods then to bpm
    if len(beats) > 1:
        if len(beats) < 4:
            print("few beats found in {:s}".format(path))
        bpms = 60. / np.diff(beats)
        return np.median(bpms)
    else:
        print("not enough beats found in {:s}".format(path))
        return None


# path: path to the file
# samplerate: samplerate of file - once normalized, this should not be a parameter
# win_s: window size in frames
# hop_s: frame jump between windows (default half of window size)
# output: can specify only BPM or only timestamp output
# Function modified from official Aubio demo file
# Source: https://github.com/aubio/aubio/blob/master/python/demos/demo_bpm_extract.py
def get_file_bpm(path, samplerate=48000, win_s=512, hop_s=256, output=None): 
    src = aubio.source(path, samplerate, hop_s)
    samplerate = src.samplerate
    o = aubio.tempo("specdiff", win_s, hop_s, samplerate)
    # List of beats, in samples
    beats = []
    # Total number of frames read
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

    bpmResult = beats_to_bpm(beats, path)
    # Could use match here instead if Python 3.10
    if output == "bpm":
        return(None, bpmResult)
    elif output == "beats":
        return(beats, None)
    else:
        return (beats, bpmResult)
