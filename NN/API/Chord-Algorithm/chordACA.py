import pyACA
import matplotlib.pyplot as plt 
import numpy as np
import os 

#internal
import functions as func
import dictionary as dict


# Requires pip install pyACA

# Not entirely sure how to plot this, believe 'label' array matched with 'time' array is correct for chord at timestamps
def getChords(path):
    #func.splitSong(path)    
    
    (label, index, time, P_E) = pyACA.computeChordsCl(path)
    print("\tpyACA algorithm results: ")
    print(label)
    print(index)
    plt.title("Identified chords - pyACA")
    plt.plot(time, label[0])        # Believe this is correct one but not sure
    #plt.plot(time, index[0])   
    print("\n")

    # If we want many chords
    # for file in os.listdir(dict.BASE_DIR + dict.SLICE_DIR):
    #     (label, index, time, P_E) = pyACA.computeChordsCl(dict.BASE_DIR + dict.SLICE_DIR + file)
    #     print(label)
    #     print(index)    
    #     # print(t)
    #     # print(P_E)
    #     plt.plot(time, label[0])
    #     #plt.plot(time, index[0])
    #     #plt.plot(time, P_E)
