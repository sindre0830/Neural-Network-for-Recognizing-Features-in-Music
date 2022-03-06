# import local modules
import dictionary as dict
# import foreign modules
import os
from pathlib import Path
from pydub import AudioSegment
import pafy


# Downloads an audio file from given URL.
def downloadAudio(id):
    # branch if audio directory doesn't exist
    if not os.path.exists(dict.NATIVE_DIR):
        os.makedirs(dict.NATIVE_DIR)
    # branch if audio file doesn't exist
    filename = id + dict.WAV_FORMAT
    if not os.path.isfile(dict.NATIVE_DIR + filename):
        url = "https://www.youtube.com/watch?v=" + id
        audiostreams = pafy.new(url).audiostreams
        # get audio format with best quality
        best = 0
        for idx, val in enumerate(audiostreams):
            temp = int(val.get_filesize())
            if best == 0 or temp > best:
                best = idx
            print(val.bitrate, val.extension, val.get_filesize())
        tempFilename = id + "." + audiostreams[best].extension
        # download audio file
        if os.path.exists(dict.NATIVE_DIR + tempFilename) is False:
            audiostreams[best].download(filepath=dict.NATIVE_DIR + tempFilename)
        # convert file to wav format and remove temporary file
        convertToWav(tempFilename)
        os.remove(dict.NATIVE_DIR + tempFilename)


# Attempts to convert a file into wav format.
def convertToWav(file):
    path = dict.NATIVE_DIR + file
    newPath = dict.NATIVE_DIR + Path(file).stem + dict.WAV_FORMAT
    if os.path.exists(newPath) is False and testExt(file):
        sound = AudioSegment.from_file(path)
        sound.export(newPath, format="wav")
    else:
        pass


# Checks if file is a supported audio format.
def testExt(file):
    if Path(file).suffix in dict.EXTENSIONS:
        return True
    else:
        return False
