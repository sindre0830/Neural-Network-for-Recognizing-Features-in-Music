# paths
BASE_DIR = "Data"

# Extensions for conversion to wav
EXTENSIONS = [".m4v", ".webm", ".mp3", ".mp4"]

# status messages
DONE = 'DONE'
SUCCESS = 'SUCCESS'
FAILED = 'FAILED'

# Print operation that allows status message on the same line.
def printOperation(message):
    print('{:<60s}'.format(message), end="", flush=True)

# Print divider in console.
def printDivider():
    print("\n") 