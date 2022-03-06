# api info
VERSION = 'v1'
# endpoint paths
DIAGNOSIS_PATH = '/' + VERSION + '/diag'
ANALYSIS_PATH = '/' + VERSION + '/analysis'
# directory paths
PLOTS_DIR = "Data/Plots/"
NATIVE_DIR = "Data/Audio/Native/"
MODIFIED_DIR = "Data/Audio/Modified/"
# extensions for conversion to wav
EXTENSIONS = [".m4v", ".webm", ".mp3", ".mp4"]
# formats
WAV_FORMAT = ".wav"
PNG_FORMAT = ".png"
# parameters
SAMPLERATE = 22050
# status messages
DONE = 'DONE'
SUCCESS = 'SUCCESS'
FAILED = 'FAILED'


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
