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


# Prepare dataset by convert from ndarray to List and setting the label names to their respective index.
def prepareDataset(data: np.ndarray, labels: np.ndarray):
    dict.printOperation("Prepare dataset...")
    # iterate through labels and set value to index
    for i in range(0, len(labels)):
        labels[i] = dict.LABEL_NAMES.index(labels[i])
    # iterate through data and Convert each matrix to List 
    for i in range(0, len(data)):
        data[i] = data[i].tolist()
    dict.printMessage(dict.DONE)
    return data.tolist(), labels
