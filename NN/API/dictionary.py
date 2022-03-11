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
# extensions for conversion to wav
EXTENSIONS = [".m4v", ".webm", ".mp3", ".mp4"]
# formats
WAV_FORMAT = ".wav"
PNG_FORMAT = ".png"
# parameters
SAMPLERATE = 10000
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


def getNativeAudioPath(id):
    return NATIVE_DIR + id + WAV_FORMAT


def getModifiedAudioPath(id):
    return MODIFIED_DIR + id + WAV_FORMAT


def getPlotPath(id):
    return PLOTS_DIR + id + PNG_FORMAT


# Print operation that allows status message on the same line.
def printOperation(message):
    print('{:<60s}'.format(message), end="", flush=True)


# Print divider in console.
def printDivider():
    print("\n")
