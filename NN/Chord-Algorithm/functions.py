# external
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np

# Splits song into 512-frame overlapping windows, and loads all with librosa
def splitSong(path, samplerate, win_s=512, hop_s=256):
    data = []
    samples = []
    # separate song here, incomplete!!!
    for index, a in enumerate(b):
        data[index], samples[index] = librosa.load(path, duration=win_s)

    
def plotChroma(data, sample):
    librosa.feature.chroma_stft(y=data, sr=sample)

    # Energy spectrogram
    S = np.abs(librosa.stft(data))

    # Power spectrogram
    S = np.abs(librosa.stft(data, n_fft=4096))**2

    chroma = librosa.feature.chroma_stft(S=S, sr=sample)

    fig, ax = plt.subplots(nrows=2, sharex=True)
    img = librosa.display.specshow(librosa.amplitude_to_db(S,ref=np.max), y_axis='log', x_axis='time', ax=ax[0])
    fig.colorbar(img, ax=[ax[0]])
    ax[0].label_outer()
    img = librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax[1])
    fig.colorbar(img, ax=[ax[1]])