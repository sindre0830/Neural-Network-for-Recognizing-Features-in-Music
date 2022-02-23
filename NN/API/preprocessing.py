# import local modules
import dictionary as dict
# import foreign modules
import os
from pathlib import Path
from pydub import AudioSegment
import pafy


# Downloads an audio file from given URL.
def downloadAudio(id):
    url = "https://www.youtube.com/watch?v=" + id
    video = pafy.new(url)
    audiostreams = video.audiostreams
    best = 0
    for idx, val in enumerate(audiostreams):
        temp = int(val.get_filesize())
        if best == 0 or temp > best:
            best = idx
        print(val.bitrate, val.extension, val.get_filesize())
    filename = (video.title + "." + audiostreams[best].extension).replace(" ", "_")
    if os.path.exists("Data/Audio/" + filename) is False:
        # DL is randomly throttled @ 60kb/s...
        audiostreams[best].download(filepath="Data/Audio/" + filename)
    else:
        print("File exists: " + filename)
    return filename


# Attempts to convert a file into wav.
def convertToWav(file):
    path = "Data/Audio/" + file
    newPath = "Data/Audio/" + Path(file).stem + ".wav"
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
