import pyACA
import matplotlib.pyplot as plt 
import numpy as np
import os 
import librosa

#internal
import functions as func
import dictionary as dict


# Requires pip install pyACA

# Not entirely sure how to plot this, believe 'label' array matched with 'time' array is correct for chord at timestamps
def getChords(path, timeframe):
    #func.splitSong(path)    
    
    (label, index, time, P_E) = pyACA.computeChordsCl(path)
    
    plt.title("Identified chords - pyACA")
    plt.xlim(timeframe)                   # only 50 - 60 sec
    plt.scatter(time, label[0])        # Believe this is correct one but not sure
    plt.show()

    # If we want many chords
    # for file in os.listdir(dict.BASE_DIR + dict.SLICE_DIR):
    #     (label, index, time, P_E) = pyACA.computeChordsCl(dict.BASE_DIR + dict.SLICE_DIR + file)
