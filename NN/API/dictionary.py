# api info
VERSION = 'v1'
# endpoint paths
DIAGNOSIS_PATH = '/' + VERSION + '/diag'
# directory paths
BASE_DIR = "Data"
# extensions for conversion to wav
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
    
