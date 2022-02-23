import pyACA
import matplotlib.pyplot as plt 
import numpy as np

# Requires pip install pyACA

# Not entirely sure how to plot this, believe 'label' array matched with 'time' array gives us chords though
def getChords(path):

    # extract feature
    (label, index, time, P_E) = pyACA.computeChordsCl(path)
    #print(label)
    #print(index)    
    # print(t)
    # print(P_E)
    plt.plot(time, label[0])
    plt.plot(time, index[0])
    #plt.plot(time, P_E)