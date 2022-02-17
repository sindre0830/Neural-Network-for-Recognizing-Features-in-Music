# external
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
from pydub.utils import mediainfo

# Loads with librosa
# If we want to split and use those for NN training, we might have to manually keep
# track of the splits by passing in individually and storing in arrays...
def songHandler(path):
    data, sample = librosa.load(path, sr = int(mediainfo(path)['sample_rate']))
    plotChroma(data, sample)
    
    
# Performs plotting
# Rather than plot, we want to just get the data out
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
    
    
# If we want to manually split the song
#def splitSong(path):
