# import local modules
import dictionary as dict
# import foreign modules
import keras.models
import keras.layers.convolutional
import keras.layers.core
import keras.optimizer_v2.adam
import keras.callbacks
import sklearn.metrics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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
def trainModel(model: keras.models.Sequential, xTrain, xTest, xVal, yTrain, yTest, yVal, verbose_flag):
    callback = keras.callbacks.EarlyStopping(min_delta=0.01, patience=3)
    # fit model by parameters
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
def predictModel(model: keras.models.Sequential, xTest, yTest):
    # predict dataset on model
    yPred = model.predict(xTest)
    # flatten each array to get index of highest value
    yPred = np.argmax(yPred, axis=1)
    yTest = np.argmax(yTest, axis=1)
    # print classification report and confusion matrix
    print(sklearn.metrics.classification_report(yTest, yPred, target_names=dict.LABEL_NAMES, zero_division=1))
    print(pd.DataFrame(sklearn.metrics.confusion_matrix(yTest, yPred), index=dict.LABEL_NAMES, columns=dict.LABEL_NAMES))


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
