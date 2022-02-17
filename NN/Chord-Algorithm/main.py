#internal
import functions as func

# external
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np

def main():
    path = "Data/P!nk_-_Raise_Your_Glass_(Official_Video).wav"
    func.songHandler(path)

if __name__ == "__main__":
    main()
