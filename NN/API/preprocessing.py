# import local modules
import dictionary as dict
# import foreign modules
import os
import librosa
import soundfile as sf
import shutil
import numpy as np


# Downloads an audio file from given URL.
def downloadAudio(id):
    # branch if audio directory doesn't exist
    if not os.path.exists(dict.NATIVE_DIR):
        os.makedirs(dict.NATIVE_DIR)
    # branch if audio file doesn't exist
    if not os.path.isfile(dict.getNativeAudioPath(id)):
        # download audio file with best quality then convert to wav
        os.system("yt-dlp -q -f 'ba' -x --audio-format wav https://www.youtube.com/watch?v=" + id + " -o '" + dict.NATIVE_DIR + "%(id)s.%(ext)s'")


# Seperates instruments and vocals from audio file.
def splitAudio(id, mode, output=None):
    # branch if audio directory doesn't exist
    if not os.path.exists(dict.MODIFIED_DIR):
        os.makedirs(dict.MODIFIED_DIR)
    if mode is not dict.NO_STEMS:
        # split audio file according to the mode then move splitt4ed file according to output
        os.system("spleeter separate -p spleeter:" + mode + " -o " + dict.MODIFIED_DIR + " " + dict.getNativeAudioPath(id))
        y, sr = librosa.load(path=dict.MODIFIED_DIR + id + output, sr=None)
        sf.write(dict.getModifiedAudioPath(id), data=y, samplerate=sr)
        # remove temporary directory
        shutil.rmtree(dict.MODIFIED_DIR + id)
    else:
        # copy native audio file to modified
        y, sr = librosa.load(path=dict.getNativeAudioPath(id), sr=None)
        sf.write(dict.getModifiedAudioPath(id), data=y, samplerate=sr)


# Resamples audio file and saves the modified version to disk.
def resampleAudio(id, samplerate):
    # branch if audio directory doesn't exist
    if not os.path.exists(dict.MODIFIED_DIR):
        os.makedirs(dict.MODIFIED_DIR)
    # check if modified audio exists and if it has correct samplerate
    flagResample = False
    if not os.path.isfile(dict.getModifiedAudioPath(id)):
        flagResample = True
    else:
        _, sr = librosa.load(path=dict.getModifiedAudioPath(id), sr=None)
        if sr is not samplerate:
            flagResample = True
    # branch if audio needs to be resampled
    if flagResample:
        y, sr = librosa.load(path=dict.getModifiedAudioPath(id), sr=None)
        # branch if audio file doesn't have the correct samplerate
        if sr is not samplerate:
            # resample audio to samplerate defined in dictionary
            y = librosa.resample(y=y, orig_sr=sr, target_sr=samplerate)
        # save resampled audio file to disk
        sf.write(dict.getModifiedAudioPath(id), data=y, samplerate=samplerate)


# Filter audio by threshold.
def filterAudio(id):
    y, sr = librosa.load(path=dict.getModifiedAudioPath(id), sr=None)
    applyFilter = np.vectorize(lambda t: 0. if t < 0.15 else t)
    y = applyFilter(y)
    sf.write(dict.getModifiedAudioPath(id), data=y, samplerate=sr)
