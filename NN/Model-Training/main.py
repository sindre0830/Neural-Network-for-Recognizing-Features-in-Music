# import local modules
import dictionary as dict
from preprocessing import (
    loadDataset,
    prepareDataset,
    splitData
)
from model import (
    generateModel,
    trainModel,
    predictModel,
    plotResults,
    saveModel
)
# import foreign modules
import os
import tensorflow as tf

# suppress info and warnings outputted by tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
# enable memory growth for gpu devices
# source: https://stackoverflow.com/a/55541385/8849692
gpu_devices = tf.config.experimental.list_physical_devices('GPU')
if gpu_devices:
    for device in gpu_devices:
        tf.config.experimental.set_memory_growth(device, True)


# Main program.
def main():
    # load dataset from file and process it to correct type
    data, labels = loadDataset()
    data, labels = prepareDataset(data, labels)
    xTrain, xTest, xVal, yTrain, yTest, yVal = splitData(data, labels)
    dict.printDivider()
    # generate model
    model = generateModel()
    model.summary()
    dict.printDivider()
    # split dataset and train model
    model, results = trainModel(model, xTrain, xTest, xVal, yTrain, yTest, yVal, verbose_flag=True)
    dict.printDivider()
    # predict on testing data and output results
    predictModel(model, xVal, yVal)
    plotResults(results)
    dict.printDivider()
    # prompt user to save the model
    saveModel(model)


# branch if program is run through 'python main.py' and run main program
if __name__ == "__main__":
    main()
