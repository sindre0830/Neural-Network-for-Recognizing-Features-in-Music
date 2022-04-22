# import local modules
import dictionary as dict
# import foreign modules
import sklearn.model_selection
import keras.utils.np_utils
import numpy as np
import os


# Load dataset from file.
def loadDataset():
    dict.printOperation("Load dataset from file...")
    (data, labels) = np.load(dict.DATASET_PATH, allow_pickle=True)
    dict.printMessage(dict.DONE)
    return data, labels


# Prepare dataset by convert from ndarray to List and setting the label names to their respective index.
def prepareDataset(data: np.ndarray, labels: np.ndarray):
    dict.printOperation("Prepare dataset (size: " + str(len(labels)) + ")...")
    # iterate through labels and set value to index
    for i in range(0, len(labels)):
        labels[i] = dict.LABEL_NAMES.index(labels[i])
    # iterate through data and Convert each matrix to List
    for i in range(0, len(data)):
        data[i] = data[i].tolist()
    # set shape
    dict.SHAPE = (12, len(data[0][0]), 1)
    dict.printMessage(dict.DONE)
    return data.tolist(), labels


# Perform tain-test-val-split.
def splitData(data, labels):
    dict.printOperation("Split dataset...")
    # branch if file exists
    if os.path.exists("Data/split.npy"):
        # load cached data
        (xTrain, xTest, xVal, yTrain, yTest, yVal) = np.load("Data/split.npy", allow_pickle=True)
    else:
        # perform train-test-val-split
        xTrain, xRem, yTrain, yRem = sklearn.model_selection.train_test_split(data, labels, train_size=dict.TRAIN_SIZE, random_state=0, stratify=labels)
        xVal, xTest, yVal, yTest = sklearn.model_selection.train_test_split(xRem, yRem, test_size=0.33, random_state=0, stratify=yRem)  
        # convert to categorical
        yTrain = keras.utils.np_utils.to_categorical(yTrain, num_classes=dict.DATASET_AMOUNT).tolist()
        yTest = keras.utils.np_utils.to_categorical(yTest, num_classes=dict.DATASET_AMOUNT).tolist()
        yVal = keras.utils.np_utils.to_categorical(yVal, num_classes=dict.DATASET_AMOUNT).tolist()
        # cache results
        splitDataset = np.array((xTrain, xTest, xVal, yTrain, yTest, yVal), dtype=object)
        np.save("Data/split.npy", splitDataset, allow_pickle=True)
    dict.printMessage(dict.DONE)
    return xTrain, xTest, xVal, yTrain, yTest, yVal
