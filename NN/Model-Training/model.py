# import foreign modules
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical


# performs train-test-split
def prepareData(data, labels, trainSize):
    xTrain, xTest, yTrain, yTest = train_test_split(data, labels, train_size = trainSize, random_state = 0)
    yTrain = to_categorical(yTrain, num_classes = 25)
    yTest = to_categorical(yTest, num_classes = 25)
    return xTrain, xTest, yTrain, yTest