# import local modules
import dictionary as dict
# import foreign modules
import os
import librosa
import soundfile as sf


# Downloads an audio file from given URL.
def downloadAudio(id):
    # branch if audio directory doesn't exist
    if not os.path.exists(dict.NATIVE_DIR):
        os.makedirs(dict.NATIVE_DIR)
    # branch if audio file doesn't exist
    if not os.path.isfile(dict.getNativeAudioPath(id)):
        # download audio file with best quality then convert to wav
        os.system("yt-dlp -q -f 'ba' -x --audio-format wav https://www.youtube.com/watch?v=" + id + " -o '" + dict.NATIVE_DIR + "%(id)s.%(ext)s'")


# Resamples audio file and saves the modified version to disk.
def resampleAudio(id):
    # branch if audio directory doesn't exist
    if not os.path.exists(dict.MODIFIED_DIR):
        os.makedirs(dict.MODIFIED_DIR)
    # check if modified audio exists and if it has correct samplerate
    flagResample = False
    if not os.path.isfile(dict.getModifiedAudioPath(id)):
        flagResample = True
    else:
        _, sr = librosa.load(path=dict.getModifiedAudioPath(id), sr=None)
        if sr is not dict.SAMPLERATE:
            flagResample = True
    # branch if audio needs to be resampled
    if flagResample:
        # load audio file with native samplerate
        y, sr = librosa.load(path=dict.getNativeAudioPath(id), sr=None)
        # branch if native audio file doesn't have the correct samplerate
        if sr is not dict.SAMPLERATE:
            # resample audio to samplerate defined in dictionary
            y = librosa.resample(y=y, orig_sr=sr, target_sr=dict.SAMPLERATE)
        # save resampled audio file to disk
        sf.write(dict.getModifiedAudioPath(id), data=y, samplerate=dict.SAMPLERATE)
