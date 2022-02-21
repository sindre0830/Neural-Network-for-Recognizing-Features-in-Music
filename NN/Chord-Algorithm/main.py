#internal
import functions as func

# external
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np

# Testing with temp files
def main():
    path = "Data/P!nk_-_Raise_Your_Glass_(Official_Video).wav"
    #path = "Data/Lorde_-_Team.wav"
    #path = "Data/Rolling_in_the_deep.wav"
    func.songHandler(path)


if __name__ == "__main__":
    main()
