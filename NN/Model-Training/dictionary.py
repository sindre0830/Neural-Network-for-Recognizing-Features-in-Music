# dataset names
LABEL_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B',
               'Cm', 'C#m', 'Dm', 'D#m', 'Em', 'Fm', 'F#m', 'Gm', 'G#m', 'Am', 'A#m', 'Bm']
# status messages
DONE = 'DONE'
SUCCESS = 'SUCCESS'
FAILED = 'FAILED'
# set parameters
SHAPE = None
DATASET_AMOUNT = len(LABEL_NAMES) + 1
LEARNING_RATE = 0.001
TRAIN_SIZE = 0.70
BATCH_SIZE = 512
EPOCHS = 50
# paths
DATASET_PATH = "Data/dataset.npy"
MODEL_PATH = "Model"


# Print operation that allows status message on the same line.
def printOperation(message):
    print('{:<60s}'.format(message), end="", flush=True)


# Print divider in console.
def printDivider():
    print("\n")


# Print message in console.
def printMessage(message: str):
    print(message)
