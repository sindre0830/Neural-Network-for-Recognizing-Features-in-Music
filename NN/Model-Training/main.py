# remove info and warnings outputted by tensorflow
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
# import local modules
import model
# import foreign modules
import librosa
import librosa.display
import matplotlib.pyplot as plt
import soundfile as sf
import shutil
import numpy as np
import json

chords = ['', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'Cm', 'C#m',
          'Dm', 'D#m', 'Em', 'Fm', 'F#m', 'Gm', 'G#m', 'Am', 'A#m', 'Bm']

# Main program.
def main():
    (data, labels) = np.load("Data/dataset.npy", allow_pickle=True)

    print(len(chords))

    print(labels[0])
    
    for i in range(0, len(labels)):
        labels[i] = chords.index(labels[i])
    
    print(labels[0])

    print(labels)

    xTrain, xTest, yTrain, yTest = model.prepareData(data, labels, 0.8)
    print(xTrain.shape)
    print(xTest.shape)
    print(yTrain.shape)
    print(yTest.shape)


# branch if program is run through 'python main.py'
if __name__ == "__main__":
    main()
