# internal libraries
import dictionary as dict
import datasetParser as data
import aubio_lib
# external libraries
from os import listdir   # not work?
import os                # work...
from aubio import source, tempo
from numpy import median, diff
from pydub.utils import mediainfo

# Leaving the testing function stuff so syntax can be checked for the API's main.py
print("Hello world")

# songs = ["https://www.youtube.com/watch?v=f2JuxM-snGc"]
# #Obviously we need checks for existing files with these - keep temp list while developing, use database later
# for song in songs:
#     temp = data.downloadAsWav(song)
#     data.convertToWav('Data/Download/' + temp, "Tests")

# path = 'Data/Tests/'
# # Should look into the arguments/parameter stuff
# for file in os.listdir(path):
#     info = mediainfo(path + file)
#     bpm = aubio_lib.get_file_bpm(path + file, orig_samplerate=int(info['sample_rate']))
#     print(file)
#     print(bpm)
#     print(info['sample_rate'])
#     dict.printDivider

#aubio_lib.pitch('Data/Tests/Beyoncé_-_Crazy_In_Love_ft._JAY_Z.wav', 44100)