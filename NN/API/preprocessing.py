import os
from pathlib import Path

#external
from pydub import AudioSegment
import librosa
import librosa.display
import IPython.display as ipd
import matplotlib.pyplot as plt
import numpy as np

#internal
from dictionary import EXTENSIONS as ext # for testExt - move func to dict?

# NOTE - paths will need to be rewritten depending on what layout we end up with WRT Data folder

# Downloads a file from given URL
def downloadAsWav(url):
    import pafy 
    video = pafy.new(url)
        
    audiostreams = video.audiostreams
    best = 0
    for idx, val in enumerate(audiostreams):
        temp = int(val.get_filesize())
        if best == 0 or temp > best:
            best = idx  
        print(val.bitrate, val.extension, val.get_filesize())
    filename = (video.title + "." +audiostreams[best].extension).replace(" ", "_")
    if os.path.exists("../Data/Download/" + filename) is False:
        audiostreams[best].download(filepath="../Data/Download/" + filename)       # DL is randomly throttled @ 60kb/s...
    else:
        print("File exists: " + filename)       # Consolidate later
    return filename

# Attempts to convert a file into wav
def convertToWav(file, folder=""):
    newpath = "../Data/" + folder + "/" + Path(file).stem + ".wav"
    if os.path.exists(newpath) is False and testExt(file):
        sound = AudioSegment.from_file(file)
        sound.export(newpath, format="wav")
    else:
        pass
   
# Helper function - ensures convert function ignores non-audio filetypes
# Move to dictionary?
def testExt(file):
    if Path(file).suffix in ext:
        return True
    else:
        return False

# Function iterating through folders containing files to be converted to wav
# ONLY needed if we make our own NN that needs training/for testing stuff
def convertDataset(path):
    dirs = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))] # only directories
    print("Folders acquired, entering...")
    print(dirs)             # debugging
    if os.path.exists("Data/" + dirs[0]) is False:  #Convert specific folder
        convertFolder(path + "/" + dirs[0])         
    #for dir in dirs:                               #Convert all folders
        #if os.path.exists("Data/" + dir) is False:
            #convertFolder(path + "/" + dir)
        
# Called by convertDataset - iterates through a folder and runs convertToWav on each file
def convertFolder(path):
    print("Folder opened, converting...")
    for file in os.listdir(path):
        convertToWav(path + "/" + file, os.path.basename(path))
        print(file + " converted to wav!")
    print("Conversion of " + os.path.basename(path) + " done!")