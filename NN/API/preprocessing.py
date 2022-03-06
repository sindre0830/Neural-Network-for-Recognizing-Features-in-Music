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
    if not os.path.exists(dict.AUDIO_DIR):
        os.makedirs(dict.AUDIO_DIR)
    # branch if audio file doesn't exist
    filename = id + ".wav"
    if not os.path.isfile(dict.AUDIO_DIR + filename):
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
        if os.path.exists(dict.AUDIO_DIR + tempFilename) is False:
            audiostreams[best].download(filepath=dict.AUDIO_DIR + tempFilename)
        # convert file to wav format and remove temporary file
        convertToWav(tempFilename)
        os.remove(dict.AUDIO_DIR + tempFilename)
    return filename


# Attempts to convert a file into wav format.
def convertToWav(file):
    path = dict.AUDIO_DIR + file
    newPath = dict.AUDIO_DIR + Path(file).stem + ".wav"
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


# Function iterating through folders containing files to be converted to wav.
def convertDataset(path):
    dirs = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
    print("Folders acquired, entering...")
    if os.path.exists("Data/" + dirs[0]) is False:
        convertFolder(path + "/" + dirs[0])


# Iterates through a folder and runs convertToWav on each file.
def convertFolder(path):
    print("Folder opened, converting...")
    for file in os.listdir(path):
        convertToWav(path + "/" + file, os.path.basename(path))
        print(file + " converted to wav!")
    print("Conversion of " + os.path.basename(path) + " done!")
