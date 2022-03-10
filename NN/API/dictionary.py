# api info
VERSION = 'v1'
# endpoint paths
DIAGNOSIS_PATH = '/' + VERSION + '/diag'
ANALYSIS_PATH = '/' + VERSION + '/analysis'
# directory paths
AUDIO_DIR = "Data/Audio/"
# extensions for conversion to wav
EXTENSIONS = [".m4v", ".webm", ".mp3", ".mp4"]
# status messages
DONE = 'DONE'
SUCCESS = 'SUCCESS'
FAILED = 'FAILED'


chords = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'Cm', 'C#m',
          'Dm', 'D#m', 'Em', 'Fm', 'F#m', 'Gm', 'G#m', 'Am', 'A#m', 'Bm']
nested_cof = ['G', 'Bm', 'D', 'F#m', 'A', 'C#m', 'E', 'G#m', 'B', 'D#m', 'F#', 'A#m',
          'C#', "Fm", "G#", 'Cm', 'D#', 'Gm', 'A#', 'Dm', 'F', 'Am', 'C', 'Em']


# Print operation that allows status message on the same line.
def printOperation(message):
    print('{:<60s}'.format(message), end="", flush=True)


# Print divider in console.
def printDivider():
    print("\n")
