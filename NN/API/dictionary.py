# api info
VERSION = 'v1'
# endpoint paths
DIAGNOSIS_PATH = '/' + VERSION + '/diag'
ANALYSIS_PATH = '/' + VERSION + '/analysis'
# directory paths
AUDIO_DIR = "Data/Audio/"
SPLIT_DIR = "Data/Audio/Split/"
# extensions for conversion to wav
EXTENSIONS = [".m4v", ".webm", ".mp3", ".mp4"]
# status messages
DONE = 'DONE'
SUCCESS = 'SUCCESS'
FAILED = 'FAILED'
# stem options for spleeter
STEMS2 = ["accompaniment", "vocals"]
STEMS4 = ["bass", "drums", "other", "vocals"]
STEMS5 = ["piano", "bass", "drums", "other", "vocals"]


# Print operation that allows status message on the same line.
def printOperation(message):
    print('{:<60s}'.format(message), end="", flush=True)


# Print divider in console.
def printDivider():
    print("\n")
