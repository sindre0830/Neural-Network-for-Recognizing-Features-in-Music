# api info
VERSION = 'v1'
# endpoint paths
DIAGNOSIS_PATH = '/' + VERSION + '/diag'
ANALYSIS_PATH = '/' + VERSION + '/analysis'
# directory paths
PLOTS_DIR = "Data/Plots/"
NATIVE_DIR = "Data/Audio/Native/"
MODIFIED_DIR = "Data/Audio/Modified/"
JSON_PATH = "Data/songs.json"
PROCESSED_JSON_PATH = "Data/processedSongs.json"
TRAINING_DATASET_PATH = "../Model-Training/Data/"
# extensions for conversion to wav
EXTENSIONS = [".m4v", ".webm", ".mp3", ".mp4"]
# formats
WAV_FORMAT = ".wav"
PNG_FORMAT = ".png"
# parameters
SAMPLERATE_BEATS = 10000
SAMPLERATE_CHORDS = 22050
# status messages
DONE = 'DONE'
SUCCESS = 'SUCCESS'
FAILED = 'FAILED'
# stem options for spleeter
NO_STEMS = None
STEMS2 = "2stems"
STEMS4 = "4stems"
STEMS5 = "5stems"
VOCALS = "/vocals" + WAV_FORMAT
OTHER = "/other" + WAV_FORMAT
BASS = "/bass" + WAV_FORMAT
DRUMS = "/drums" + WAV_FORMAT
PIANO = "/piano" + WAV_FORMAT
ACCOMPANIMENT = "/accompaniment" + WAV_FORMAT

FLAG_DATABASE = False
# blacklisted songs from EC-Play dataset
BLACKLIST = ["6d5ST3tbPIU", "ASywAfBAVrQ", "DGIgXP9SvB8", "qf9Ipqubh9g", "gaR2k-EPADs", "V9RxDNY2vuk", "Lrl5C-cYC64", "nnDyWwZs-ek "]


def getNativeAudioPath(id):
    return NATIVE_DIR + id + WAV_FORMAT


def getModifiedAudioPath(id):
    return MODIFIED_DIR + id + WAV_FORMAT


def getPlotPath(id):
    return PLOTS_DIR + id + PNG_FORMAT


chords = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'Cm', 'C#m',
          'Dm', 'D#m', 'Em', 'Fm', 'F#m', 'Gm', 'G#m', 'Am', 'A#m', 'Bm']
nested_cof = ['G', 'Bm', 'D', 'F#m', 'A', 'C#m', 'E', 'G#m', 'B', 'D#m', 'F#', 'A#m',
              'C#', "Fm", "G#", 'Cm', 'D#', 'Gm', 'A#', 'Dm', 'F', 'Am', 'C', 'Em']


# Print operation that allows status message on the same line.
def printOperation(message, verbose=True):
    if verbose:
        print('{:<60s}'.format(message), end="", flush=True)


# Print message if verbose parameter is set to true.
def printMessage(message, verbose=True):
    if verbose:
        print(message)


# Print divider in console.
def printDivider(verbose=True):
    if verbose:
        print("\n")
