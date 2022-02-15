import aubio_lib
# external libraries
from pydub.utils import mediainfo

# Handler for aubio analysis
def analyseBeats(path):
    info = mediainfo(path)          # We get sample rate from file
    # gets timestamps and bpm - use arguments if only one is wanted
    (beats, bpm) = aubio_lib.get_file_bpm(path, samplerate=int(info['sample_rate']))
    
    # Decide what to do with output here - currently just prints
    print(path)
    if bpm is not None:
        print(bpm)
    if beats is not None:
        print(beats)   
    print(info['sample_rate'])
    