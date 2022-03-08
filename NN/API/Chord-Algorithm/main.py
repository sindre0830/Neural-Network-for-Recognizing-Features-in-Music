#internal
import functions as func
import hmm
import match_templates as temp
import dictionary as dict

# external
import chordACA
import librosa
import soundfile as sf
from pydub.utils import mediainfo
import matplotlib.pyplot as plt
import numpy as np

# temp
import libfmp.b
import libfmp.c3
import libfmp.c4
import os



# Testing with temp files
def main():
    #path = "../Data/Audio/output/N8BXtM6onEY"             # Sia
    path = "../Data/Audio/output/fRXtQpw7X3k"            # White Stripes
    
    # Used for debug/testing sample rate
    #y, sr = librosa.load(path)
    #path = "../Data/Audio/test.wav"
    #sf.write(path, y, sr)
    #timeframe = (29, 39)   # Sia
    #timeframe = (46, 50)    # White Stripes
    
    #func.songHandler(path, timeframe)               # Check with handling the different algorithms 
    func.librosaVocalFilter(path)

    
if __name__ == "__main__":
    main()
