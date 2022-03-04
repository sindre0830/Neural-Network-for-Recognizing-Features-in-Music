#internal
import functions as func
import hmm
import match_templates as temp
import chordACA
import librosa
import soundfile as sf
from pydub.utils import mediainfo
import matplotlib.pyplot as plt

# Testing with temp files
def main():
    path = "../Data/Audio/N8BXtM6onEY.wav"
    
    # Used for debug/testing sample rate
    #y, sr = librosa.load(path)
    #path = "../Data/Audio/test.wav"
    #sf.write(path, y, sr)
    #timeframe = (29, 39)
    
    func.songHandler(path)               # Check with handling the different algorithms 


if __name__ == "__main__":
    main()
