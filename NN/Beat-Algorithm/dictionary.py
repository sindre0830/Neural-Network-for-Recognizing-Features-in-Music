# paths
BASE_DIR = "Data"

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
    