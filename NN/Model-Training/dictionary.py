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
TRAIN_SIZE = 0.70
VAL_SIZE = 0.66
TEST_SIZE = 0.33
BATCH_SIZE = 512
EPOCHS = 50
# paths
DATASET_PATH = "Data/dataset.npy"
SPLIT_PATH = "Data/split.npy"
RANDOM_SEARCH_PATH = "Data/RandomSearch/"
MODEL_PATH = "../API/Model"


# Print operation that allows status message on the same line.
def printOperation(message):
    print('{:<60s}'.format(message), end="", flush=True)


# Print divider in console.
def printDivider():
    print("\n")


# Print message in console.
def printMessage(message: str):
    print(message)
