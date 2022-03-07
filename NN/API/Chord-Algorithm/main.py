#internal
import functions as func
import hmm
import match_templates as temp
import chordACA
import librosa
import soundfile as sf
from pydub.utils import mediainfo
import matplotlib.pyplot as plt
import numpy as np
import dictionary as dict


# temp
import libfmp.b
import libfmp.c3
import libfmp.c4
import os



# Testing with temp files
def main():
    path = "../Data/Audio/N8BXtM6onEY.wav"
    
    # Used for debug/testing sample rate
    #y, sr = librosa.load(path)
    #path = "../Data/Audio/test.wav"
    #sf.write(path, y, sr)
    #timeframe = (29, 39)
    
    #func.songHandler(path)               # Check with handling the different algorithms 
    func.librosaVocalFilter(path)
    
if __name__ == "__main__":
    main()
