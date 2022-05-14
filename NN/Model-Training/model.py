# import local modules
import dictionary as dict
# import foreign modules
import keras.models
import keras.layers.convolutional
import keras.layers.core
import keras.layers
import keras.regularizers
import keras.optimizer_v2.adam
import keras.callbacks
import sklearn.metrics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import random
import gc
import datetime
import os


# Perform random search to find the best model.
def randomSearch(xTrain, xTest, xVal, yTrain, yTest, yVal):
    layers = [0, 1, 2]
    filters = [16, 32, 64, 128, 256]
    units = [32, 64, 128, 256]
    regularizers = [0.0001, 0.0005, 0.001, 0.005]
    results = []
    i = 0
    N = 20
    # generate each possible combination, randomize, and choose N combinations to test
    combinations = list(itertools.product(filters, regularizers, layers, filters, layers, filters, layers,
                                          filters, layers, units, layers, units, layers, units))
    random.shuffle(combinations)
    combinations = combinations[:N]
    # iterate through each combination and train each model while saving the results
    for (initial_filter, regularizer, conv_layer_1, conv_filter_1, conv_layer_2, conv_filter_2, conv_layer_3, conv_filter_3,
         dense_layer_1, dense_units_1, dense_layer_2, dense_units_2, dense_layer_3, dense_units_3) in combinations:
        i += 1
        dict.printOperation("Training model " + str(i) + "...")
        # create and train model based on parameters
        val_loss, val_accuracy = generateRandomSearchModel(
            initial_filters=initial_filter,
            regularizer=regularizer,
            conv_layer_1=conv_layer_1,
            conv_filters_1=conv_filter_1,
            conv_layer_2=conv_layer_2,
            conv_filters_2=conv_filter_2,
            conv_layer_3=conv_layer_3,
            conv_filters_3=conv_filter_3,
            dense_layer_1=dense_layer_1,
            dense_units_1=dense_units_1,
            dense_layer_2=dense_layer_2,
            dense_units_2=dense_units_2,
            dense_layer_3=dense_layer_3,
            dense_units_3=dense_units_3,
            xTrain=xTrain, xTest=xTest, xVal=xVal, yTrain=yTrain, yTest=yTest, yVal=yVal
        )
        # create object and store result and parameters
        result = {}
        result["val_accuracy"] = val_accuracy
        result["val_loss"] = val_loss
        result["initial_filter"] = initial_filter
        result["conv_layer_1"] = conv_layer_1
        result["conv_filter_1"] = conv_filter_1
        result["conv_layer_2"] = conv_layer_2
        result["conv_filter_2"] = conv_filter_2
        result["conv_layer_3"] = conv_layer_3
        result["conv_filter_3"] = conv_filter_3
        result["dense_layer_1"] = dense_layer_1
        result["dense_units_1"] = dense_units_1
        result["dense_layer_2"] = dense_layer_2
        result["dense_units_2"] = dense_units_2
        result["dense_layer_3"] = dense_layer_3
        result["dense_units_3"] = dense_units_3
        result["regularizer"] = regularizer
        results.append(result)
        dict.printMessage(dict.DONE)
    # sort results by accuracy and convert to string
    results = sorted(results, key=lambda x: x["val_accuracy"], reverse=True)
    strResults = ""
    for val in results:
        strResults += "val_accuracy: {} \t| val_loss: {} \t| ".format(val["val_accuracy"], val["val_loss"])
        strResults += "initial_filter: {} \t| conv_layer_1: {} \t| ".format(val["initial_filter"], val["conv_layer_1"])
        strResults += "conv_filter_1: {} \t| conv_layer_2: {} \t| ".format(val["conv_filter_1"], val["conv_layer_2"])
        strResults += "conv_filter_2: {} \t| conv_layer_3: {} \t| ".format(val["conv_filter_2"], val["conv_layer_3"])
        strResults += "conv_filter_3: {} \t| dense_layer_1: {} \t| ".format(val["conv_filter_3"], val["dense_layer_1"])
        strResults += "dense_units_1: {} \t| dense_layer_2: {} \t| ".format(val["dense_units_1"], val["dense_layer_2"])
        strResults += "dense_units_2: {} \t| dense_layer_3: {} \t| ".format(val["dense_units_2"], val["dense_layer_3"])
        strResults += "dense_units_3: {} \t| regularizer: {}\n".format(val["dense_units_3"], val["regularizer"])
    # Create a folder if it doesn't exist and save the results to a txt file
    if not os.path.exists(dict.RANDOM_SEARCH_PATH):
        os.makedirs(dict.RANDOM_SEARCH_PATH)
    with open(dict.RANDOM_SEARCH_PATH + datetime.datetime.now().strftime("%H:%M:%S") + ".txt", "w+") as outfile:
        outfile.write(strResults)
    dict.printDivider()


# Generate convolutional neural network model and return results. Used for random search.
def generateRandomSearchModel(
        initial_filters: int,
        regularizer: float,
        conv_layer_1: int,
        conv_filters_1: int,
        conv_layer_2: int,
        conv_filters_2: int,
        conv_layer_3: int,
        conv_filters_3: int,
        dense_layer_1: int,
        dense_units_1: int,
        dense_layer_2: int,
        dense_units_2: int,
        dense_layer_3: int,
        dense_units_3: int,
        xTrain, xTest, xVal, yTrain, yTest, yVal
        ):
    model = keras.models.Sequential()
    # initial layer and conv layers
    model.add(keras.layers.convolutional.Conv2D(
        filters=initial_filters,
        kernel_size=3,
        input_shape=dict.SHAPE,
        kernel_regularizer=keras.regularizers.l2(regularizer)
    ))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Activation('relu'))
    for _ in range(conv_layer_1):
        model.add(keras.layers.convolutional.Conv2D(filters=conv_filters_1, kernel_size=1))
        model.add(keras.layers.BatchNormalization())
        model.add(keras.layers.Activation('relu'))
        model.add(keras.layers.Dropout(rate=0.1))
    for _ in range(conv_layer_2):
        model.add(keras.layers.convolutional.Conv2D(filters=conv_filters_2, kernel_size=1))
        model.add(keras.layers.BatchNormalization())
        model.add(keras.layers.Activation('relu'))
        model.add(keras.layers.Dropout(rate=0.1))
    for _ in range(conv_layer_3):
        model.add(keras.layers.convolutional.Conv2D(filters=conv_filters_3, kernel_size=1))
        model.add(keras.layers.BatchNormalization())
        model.add(keras.layers.Activation('relu'))
        model.add(keras.layers.Dropout(rate=0.1))
    # flatten layer and dense layers
    model.add(keras.layers.core.Flatten())
    for _ in range(dense_layer_1):
        model.add(keras.layers.core.Dense(units=dense_units_1))
        model.add(keras.layers.BatchNormalization())
        model.add(keras.layers.Activation('relu'))
        model.add(keras.layers.Dropout(rate=0.25))
    for _ in range(dense_layer_2):
        model.add(keras.layers.core.Dense(units=dense_units_2))
        model.add(keras.layers.BatchNormalization())
        model.add(keras.layers.Activation('relu'))
        model.add(keras.layers.Dropout(rate=0.25))
    for _ in range(dense_layer_3):
        model.add(keras.layers.core.Dense(units=dense_units_3))
        model.add(keras.layers.BatchNormalization())
        model.add(keras.layers.Activation('relu'))
        model.add(keras.layers.Dropout(rate=0.25))
    # last layer
    model.add(keras.layers.core.Dense(units=dict.DATASET_AMOUNT, activation='sigmoid'))
    model.compile(
        optimizer=keras.optimizer_v2.adam.Adam(),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    # fit model by parameters
    callback = keras.callbacks.EarlyStopping(min_delta=0.01, patience=5)
    model.fit(
        xTrain,
        yTrain,
        validation_data=(xTest, yTest),
        batch_size=dict.BATCH_SIZE,
        epochs=dict.EPOCHS,
        verbose=0,
        callbacks=[callback]
    )
    # evaluate model and output results
    results = model.evaluate(xVal, yVal, verbose=0)
    # delete model and run garbage collection
    del model
    gc.collect()
    return results[0], results[1]


# Generate convolutional neural network model.
def generateModel():
    model = keras.models.Sequential([
        # layer 1
        keras.layers.convolutional.Conv2D(
            filters=64,
            kernel_size=3,
            input_shape=dict.SHAPE,
            kernel_regularizer=keras.regularizers.l2(0.0005)
        ),
        keras.layers.BatchNormalization(),
        keras.layers.Activation('relu'),
        keras.layers.Dropout(rate=0.1),
        # layer 2
        keras.layers.convolutional.Conv2D(filters=32, kernel_size=1),
        keras.layers.BatchNormalization(),
        keras.layers.Activation('relu'),
        keras.layers.Dropout(rate=0.1),
        # layer 3
        keras.layers.convolutional.Conv2D(filters=64, kernel_size=1),
        keras.layers.BatchNormalization(),
        keras.layers.Activation('relu'),
        keras.layers.Dropout(rate=0.1),
        # layer 3
        keras.layers.convolutional.Conv2D(filters=64, kernel_size=1),
        keras.layers.BatchNormalization(),
        keras.layers.Activation('relu'),
        keras.layers.Dropout(rate=0.1),
        # layer 3
        keras.layers.convolutional.Conv2D(filters=16, kernel_size=1),
        keras.layers.BatchNormalization(),
        keras.layers.Activation('relu'),
        keras.layers.Dropout(rate=0.1),
        # layer 3
        keras.layers.convolutional.Conv2D(filters=16, kernel_size=1),
        keras.layers.BatchNormalization(),
        keras.layers.Activation('relu'),
        keras.layers.Dropout(rate=0.1),
        # flatten
        keras.layers.core.Flatten(),
        # layer 4
        keras.layers.core.Dense(units=256),
        keras.layers.BatchNormalization(),
        keras.layers.Activation('relu'),
        keras.layers.Dropout(rate=0.25),
        # layer 4
        keras.layers.core.Dense(units=256),
        keras.layers.BatchNormalization(),
        keras.layers.Activation('relu'),
        keras.layers.Dropout(rate=0.25),
        # layer 5
        keras.layers.core.Dense(units=dict.DATASET_AMOUNT, activation='sigmoid')
    ])
    model.compile(
        optimizer=keras.optimizer_v2.adam.Adam(),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model


# Function to run model.fit.
def trainModel(model: keras.models.Sequential, xTrain, xTest, xVal, yTrain, yTest, yVal, verbose_flag):
    # fit model by parameters
    callback = keras.callbacks.EarlyStopping(min_delta=0.01, patience=5)
    results = model.fit(
        xTrain,
        yTrain,
        validation_data=(xTest, yTest),
        batch_size=dict.BATCH_SIZE,
        epochs=dict.EPOCHS,
        verbose=verbose_flag,
        callbacks=[callback]
    )
    # evaluate model and output results
    model.evaluate(xVal, yVal)
    return model, results


# Function for running model.predict.
def predictModel(model: keras.models.Sequential, xVal, yVal):
    # predict dataset on model
    yPred = model.predict(xVal)
    # flatten each array to get index of highest value
    yPred = np.argmax(yPred, axis=1)
    yVal = np.argmax(yVal, axis=1)
    # print classification report and confusion matrix
    print(sklearn.metrics.classification_report(yVal, yPred, target_names=dict.LABEL_NAMES, zero_division=1))
    print(pd.DataFrame(sklearn.metrics.confusion_matrix(yVal, yPred), index=dict.LABEL_NAMES, columns=dict.LABEL_NAMES))


# Plots a graph with the results from model training.
def plotResults(results):
    # get values from results
    history_dict = results.history
    loss_values = history_dict['loss']
    val_loss_values = history_dict['val_loss']
    val_accuracy = history_dict['val_accuracy']
    epochs = range(1, (len(history_dict['loss']) + 1))
    # plot training and validation loss
    plt.clf()
    plt.plot(epochs, loss_values, label='Training loss', c='lightgreen')
    plt.plot(epochs, val_loss_values, label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()
    # plot validation accuracy
    plt.clf()
    plt.plot(epochs, val_accuracy, label='Validation accuracy', c='red')
    plt.title('Validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.ylim(0, 1)
    plt.legend()
    plt.show()


# Save model to disk in HDF5 format.
def saveModel(model: keras.models.Sequential):
    inp = input("Do you want to save the model? Y/N: ")
    if inp.lower() == "y":
        dict.printOperation("Saving model...")
        model.save(dict.MODEL_PATH)
        dict.printMessage(dict.DONE)
