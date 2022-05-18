# api info
VERSION = 'v1'
# endpoint paths
DIAGNOSIS_ENDPOINT = '/' + VERSION + '/diag'
ANALYSIS_ENDPOINT = '/' + VERSION + '/analysis'
REMOVE_ENDPOINT = '/' + VERSION + '/remove'
# directory paths
TRIMMED_SONGS_PATH = "Data/Processed/"
PLOTS_PATH = "Data/Plots/"
NATIVE_PATH = "Data/Audio/Native/"
MODIFIED_PATH = "Data/Audio/Modified/"
JSON_PATH = "Data/songs.json"
RESULTS_PATH = "Data/Results/"
RESULTS_SONG_PATH = RESULTS_PATH + "Songs/"
RESULTS_BEATS_PATH = RESULTS_PATH + "Beats/"
PROCESSED_JSON_PATH = "Data/processedSongs.json"
CHORD_JSON_PATH = "Data/evaluatedChords.json"
BEAT_JSON_PATH = "Data/evaluatedBeats.json"
CHORDRESULTS_CSV_PATH = "Data/Results/chordResults.csv"
BEATRESULTS_CSV_PATH = "Data/Results/beatResults.csv"
DETAILED_RESULTS_PATH = "Data/Results/detailedResults.json"
CHORDPLOT_PATH = "Data/Results/chordplot.png"
BEATPLOT_PATH = "Data/Results/beatplot.png"
TRAINING_DATASET_PATH = "../Model-Training/Data/"
MODEL_PATH = "Model/"
# extensions for conversion to wav
EXTENSIONS = [".m4v", ".webm", ".mp3", ".mp4"]
# formats
WAV_FORMAT = ".wav"
PNG_FORMAT = ".png"
JSON_FORMAT = ".json"
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
FLAG_RESULTS = False
# blacklisted songs from EC-Play dataset
BLACKLIST = ["6d5ST3tbPIU", "ASywAfBAVrQ", "DGIgXP9SvB8", "qf9Ipqubh9g", "gaR2k-EPADs", "V9RxDNY2vuk", "Lrl5C-cYC64", "nnDyWwZs-ek ", "poZOXqafw-4"]


def getNativeAudioPath(id):
    return NATIVE_PATH + id + WAV_FORMAT


def getModifiedAudioPath(id):
    return MODIFIED_PATH + id + WAV_FORMAT


def getSongResultAudioPath(id):
    return RESULTS_SONG_PATH + id + JSON_FORMAT


def getPlotPath(id):
    return PLOTS_PATH + id + PNG_FORMAT


# chords
chords = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'Cm', 'C#m',
          'Dm', 'D#m', 'Em', 'Fm', 'F#m', 'Gm', 'G#m', 'Am', 'A#m', 'Bm', '']

algoFormat = {'C Maj': 'C',
              'C# Maj': 'C#',
              'D Maj': 'D',
              'D# Maj': 'D#',
              'E Maj': 'E',
              'F Maj': 'F',
              'F# Maj': 'F#',
              'G Maj': 'G',
              'G# Maj': 'G#',
              'A Maj': 'A',
              'A# Maj': 'A#',
              'B Maj': 'B',
              'c min': 'Cm',
              'c# min': 'C#m',
              'd min': 'Dm',
              'd# min': 'D#m',
              'e min': 'Em',
              'f min': 'Fm',
              'f# min': 'F#m',
              'g min': 'Gm',
              'g# min': 'G#m',
              'a min': 'Am',
              'a# min': 'A#m',
              'b min': 'Bm'}


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
