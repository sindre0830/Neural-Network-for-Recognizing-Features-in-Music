# paths
BASE_DIR = "Data"

# status messages
DONE = 'DONE'
SUCCESS = 'SUCCESS'
FAILED = 'FAILED'

win_s = 6           # Seconds per window
hop_s = win_s // 2  # 50% overlap

pitches = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

# Print operation that allows status message on the same line.
def printOperation(message):
    print('{:<60s}'.format(message), end="", flush=True)


# Print divider in console.
def printDivider():
    print("\n") 
