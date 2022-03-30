# import local modules
import dictionary as dict
# import foreign modules
import keras.models
import keras.layers.convolutional
import keras.layers.core
import keras.optimizer_v2.adam
import sklearn.metrics
import numpy as np
import pandas as pd


# Generate convolutional neural network model.
def generateModel():
    model = keras.models.Sequential([
        # layer 1
        keras.layers.convolutional.Conv2D(filters=32, kernel_size=3, input_shape=dict.SHAPE, activation='relu'),
        # layer 2
        keras.layers.convolutional.Conv2D(filters=32, kernel_size=3, activation='relu'),
        # layer 3
        keras.layers.convolutional.Conv2D(filters=64, kernel_size=3, activation='relu'),
        # flatten
        keras.layers.core.Flatten(),
        # layer 4
        keras.layers.core.Dense(units=64, activation='relu'),
        keras.layers.core.Dropout(rate=0.5),
        # layer 5
        keras.layers.core.Dense(units=dict.DATASET_AMOUNT, activation='sigmoid')
    ])
    model.compile(
        optimizer=keras.optimizer_v2.adam.Adam(learning_rate=dict.LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model


# Function to run model.fit.
def trainModel(model: keras.models.Sequential, xTrain, xTest, yTrain, yTest, verbose_flag):
    # fit model by parameters
    results = model.fit(
        xTrain, 
        yTrain, 
        validation_data=(xTest, yTest), 
        batch_size=dict.BATCH_SIZE, 
        epochs=dict.EPOCHS,
        verbose=verbose_flag
    )
    # evaluate model and output results
    model.evaluate(xTest, yTest)
    return model, results


# Function for running model.predict.
def predictModel(model: keras.models.Sequential, xTest, yTest):
    # predict dataset on model
    yPred = model.predict(xTest)
    # flatten each array to get index of highest value
    yPred = np.argmax(yPred, axis=1)
    yTest = np.argmax(yTest, axis=1)
    # print classification report and confusion matrix
    print(sklearn.metrics.classification_report(yTest, yPred, target_names=dict.LABEL_NAMES, zero_division=1))
    print(pd.DataFrame(sklearn.metrics.confusion_matrix(yTest, yPred), index=dict.LABEL_NAMES, columns=dict.LABEL_NAMES))
