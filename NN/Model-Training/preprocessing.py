# import local modules
import dictionary as dict
# import foreign modules
import numpy as np


# Load dataset from file.
def loadDataset():
    dict.printOperation("Load dataset from file...")
    (data, labels) = np.load(dict.DATASET_PATH, allow_pickle=True)
    dict.printMessage(dict.DONE)
    return data, labels
