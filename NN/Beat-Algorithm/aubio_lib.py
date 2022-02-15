from aubio import source, tempo
from numpy import median, diff
import sys

# get_file_bpm
# path: path to the file
# samplerate: samplerate of file - once normalized, this should not be a parameter
# win_s: window size in frames
# hop_s: frame jump between windows (default half of window size)
# output: can specify only BPM or only timestamp output
# Function modified from official Aubio demo file
# Source: https://github.com/aubio/aubio/blob/master/python/demos/demo_bpm_extract.py
def get_file_bpm(path, samplerate=48000, win_s=512, hop_s=256, output=None):
        
    s = source(path, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("specdiff", win_s, hop_s, samplerate)
    # List of beats, in samples
    beats = []
    # Total number of frames read
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
            #if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < hop_s:
            break
        
    
    # Improve error handling here
    def beats_to_bpm(beats, path):
        # if enough beats are found, convert to periods then to bpm
        if len(beats) > 1:
            if len(beats) < 4:
                print("few beats found in {:s}".format(path))
            bpms = 60./diff(beats)
            return median(bpms)
        else:
            print("not enough beats found in {:s}".format(path))
            return None
        
    
    bpmResult = beats_to_bpm(beats, path)
    # Could use match here instead if Python 3.10
    if output == "bpm":
        return(None, bpmResult)
    elif output == "beats":
        return(beats, None)
    else:
        return (beats, bpmResult)


# Notes
# Returns three columns - onset, pitch, duration
# May be useful for pattern? Not sure
# Function taken from official Aubio demo file
# Source:https://github.com/aubio/aubio/blob/master/python/demos/demo_notes.py
def notes (path, orig_sample):
    from aubio import source, notes

    filename = path

    downsample = 1
    samplerate = orig_sample // downsample

    win_s = 512 // downsample # fft size
    hop_s = 256 // downsample # hop size

    s = source(filename, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.8

    notes_o = notes("default", win_s, hop_s, samplerate)

    print("%8s" % "time","[ start","vel","last ]")

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        new_note = notes_o(samples)
        if (new_note[0] != 0):
            note_str = ' '.join(["%.2f" % i for i in new_note])
            print("%.6f" % (total_frames/float(samplerate)), new_note)
        total_frames += read
        if read < hop_s: break
  
     
# Pitch
# Finds frequency(pitch) for each frame
# Unsure of the output format though! 1st column timestamp, 2nd pitch, 3rd ???
# We also get plot
# Function taken from official Aubio demo file
# Source: https://github.com/aubio/aubio/blob/master/python/demos/demo_pitch.py
def pitch(path, orig_sample):
        
    from aubio import source, pitch
    filename = path

    downsample = 1
    samplerate = orig_sample // downsample

    win_s = 4096 // downsample # fft size
    hop_s = 512  // downsample # hop size

    s = source(filename, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.8

    pitch_o = pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)

    pitches = []
    confidences = []

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        #pitch = int(round(pitch))
        confidence = pitch_o.get_confidence()
        #if confidence < 0.8: pitch = 0.
        print("%f %f %f" % (total_frames / float(samplerate), pitch, confidence))
        pitches += [pitch]
        confidences += [confidence]
        total_frames += read
        if read < hop_s: break

    if 0: sys.exit(0)

    #print pitches
    import os.path
    from numpy import array, ma
    import matplotlib.pyplot as plt
    from demo_waveform_plot import get_waveform_plot, set_xlabels_sample2time

    skip = 1

    pitches = array(pitches[skip:])
    confidences = array(confidences[skip:])
    times = [t * hop_s for t in range(len(pitches))]

    fig = plt.figure()

    ax1 = fig.add_subplot(311)
    ax1 = get_waveform_plot(filename, samplerate = samplerate, block_size = hop_s, ax = ax1)
    plt.setp(ax1.get_xticklabels(), visible = False)
    ax1.set_xlabel('')

    def array_from_text_file(filename, dtype = 'float'):
        filename = os.path.join(os.path.dirname(__file__), filename)
        return array([line.split() for line in open(filename).readlines()],
            dtype = dtype)

    ax2 = fig.add_subplot(312, sharex = ax1)
    ground_truth = os.path.splitext(filename)[0] + '.f0.Corrected'
    if os.path.isfile(ground_truth):
        ground_truth = array_from_text_file(ground_truth)
        true_freqs = ground_truth[:,2]
        true_freqs = ma.masked_where(true_freqs < 2, true_freqs)
        true_times = float(samplerate) * ground_truth[:,0]
        ax2.plot(true_times, true_freqs, 'r')
        ax2.axis( ymin = 0.9 * true_freqs.min(), ymax = 1.1 * true_freqs.max() )
    # plot raw pitches
    ax2.plot(times, pitches, '.g')
    # plot cleaned up pitches
    cleaned_pitches = pitches
    #cleaned_pitches = ma.masked_where(cleaned_pitches < 0, cleaned_pitches)
    #cleaned_pitches = ma.masked_where(cleaned_pitches > 120, cleaned_pitches)
    cleaned_pitches = ma.masked_where(confidences < tolerance, cleaned_pitches)
    ax2.plot(times, cleaned_pitches, '.-')
    #ax2.axis( ymin = 0.9 * cleaned_pitches.min(), ymax = 1.1 * cleaned_pitches.max() )
    #ax2.axis( ymin = 55, ymax = 70 )
    plt.setp(ax2.get_xticklabels(), visible = False)
    ax2.set_ylabel('f0 (midi)')

    # plot confidence
    ax3 = fig.add_subplot(313, sharex = ax1)
    # plot the confidence
    ax3.plot(times, confidences)
    # draw a line at tolerance
    ax3.plot(times, [tolerance]*len(confidences))
    ax3.axis( xmin = times[0], xmax = times[-1])
    ax3.set_ylabel('confidence')
    set_xlabels_sample2time(ax3, times[-1], samplerate)
    plt.show()
    #plt.savefig(os.path.basename(filename) + '.svg')           # if we want to save
