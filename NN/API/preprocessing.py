# import local modules
import dictionary as dict
import beat_algorithm
import chord_algorithm
# import foreign modules
import os
import librosa
import soundfile as sf
import shutil
import numpy as np
import json


# Downloads an audio file from given URL.
def downloadAudio(id):
    # branch if audio directory doesn't exist
    if not os.path.exists(dict.NATIVE_DIR):
        os.makedirs(dict.NATIVE_DIR)
    # branch if audio file doesn't exist
    if not os.path.isfile(dict.getNativeAudioPath(id)):
        # download audio file with best quality then convert to wav
        os.system("yt-dlp -q -f 'ba' -x --audio-format wav https://www.youtube.com/watch?v=" +
                  id + " -o '" + dict.NATIVE_DIR + "%(id)s.%(ext)s'")


# Seperates instruments and vocals from audio file.
def splitAudio(id, mode, output=None):
    # branch if audio directory doesn't exist
    if not os.path.exists(dict.MODIFIED_DIR):
        os.makedirs(dict.MODIFIED_DIR)
    if mode is not dict.NO_STEMS:
        # split audio file according to the mode then move splitt4ed file according to output
        os.system("spleeter separate -p spleeter:" + mode + " -o " +
                  dict.MODIFIED_DIR + " " + dict.getNativeAudioPath(id))
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


# Parses songs.json to a simplified JSON object.
def parseJson(path):
    if os.path.exists(dict.JSON_PATH):
        dict.FLAG_DATABASE = True
        with open(path, 'r') as f:
            document = json.loads(f.read())

        current = {}
        with open(dict.PROCESSED_JSON_PATH, "w+") as f:
            if os.path.getsize(dict.PROCESSED_JSON_PATH) != 0:
                current = json.loads(f.read())

        songs = {}

        for key in document:
            s = {}
            song = flattenSongData(key)
            s["chords"] = song["chords"]
            s["beats"] = song["beats"]
            songs[song["id"]] = s

        print("Parsed " + str(len(songs)) + " songs from songs.json.")
        print("Parsed " + str(len(current)) + " songs from processedSongs.json.")

        # Overwrite if new data
        if len(songs) > len(current):
            json_object = json.dumps(songs, indent=3)
            with open(dict.PROCESSED_JSON_PATH, "r+") as outfile:
                outfile.write(json_object)
            print("Successfully updated processedSongs.json")
        else:
            print("No new data")
    else:
        print("Missing songs.json")


# Extracts relevant song data for testing from songs.json.
def flattenSongData(song):
    arrangement = song["arrangement"]
    parts = song["parts"]
    beats = song["beats"]
    flattenedChords = []

    # going through every part and repetition in song
    for arr in arrangement:
        partIndex = int(arr["part"])
        part = parts[partIndex]
        repetitions = int(arr["repetitions"])
        bars = part["bars"]
        chordsInRepetition = []

        # going though every chord in the part
        for bar in bars:
            chords = bar["chords"]
            length = bar["length"]
            for chord in chords:
                if ("pause" in chord and chord["pause"]) or chord["chord"] == "pause":
                    for _ in range(length):
                        chordsInRepetition.append("")
                else:
                    for _ in range(length):
                        chordsInRepetition.append(chordToString(int(chord["chord"]), chord["minor"]))

        # adding a duplicate for each repetition
        for _ in range(repetitions):
            flattenedChords += chordsInRepetition

    return {"id": song["youtubeLink"], "chords": flattenedChords, "beats": beats}


# Turns a chord on the format in the EC-Play app into one of the chords in the array.
def chordToString(chordNum: int, minor: bool):
    if chordNum > 11 or chordNum < 0:
        return ""

    charNum = chordNum//2 + 1

    if chordNum <= 2 or chordNum == 4 or chordNum == 6:
        charNum -= 1

    if minor:
        char = chr(charNum + 97)
    else:
        char = chr(charNum + 65)

    if chordNum == 1 or chordNum == 4 or chordNum == 6 or chordNum == 9 or chordNum == 11:
        char += "#"

    if minor:
        char += " min"
    else:
        char += " Maj"

    return char


# Handles batch process comparison of database
def batchHandler(force:bool = False):
    # Make sure we have the dataset parsed
    if not os.path.exists(dict.PROCESSED_JSON_PATH):
        parseJson(dict.JSON_PATH)

    with open(dict.PROCESSED_JSON_PATH, 'r') as f:
        dataset = json.loads(f.read())
        
    with open(dict.ALGORITHM_JSON_PATH, 'r') as f:
        results = json.loads(f.read())

    dictionary = {}
    # Check if we have existing data for comparison and data does not need to be reprocessed
    if os.path.getsize(dict.ALGORITHM_JSON_PATH) != 0 and not force:
        if len(dataset) == len(results):
            dict.FLAG_RESULTS = True
            
    # # Go through dataset
    for key in dataset:
        # Get the data we need if not existing
        if not dict.FLAG_RESULTS:
            downloadAudio(id)
            beatRecognizer = beat_algorithm.BeatRecognizer(id)
            beatRecognizer.run()
            splitAudio(id, mode=dict.STEMS2, output=dict.ACCOMPANIMENT)
            resampleAudio(id, dict.SAMPLERATE_CHORDS)
            chords = chord_algorithm.chordHandler(id, beatRecognizer.beats)
            # Add to dictionary
            createJson(dict, id, chords, beatRecognizer.beats)
        # This is where the comparison happens!

        
    # Write our new algorithm data to file
    if not dict.FLAG_RESULTS:
        with open(dict.ALGORITHM_JSON_PATH, 'w') as f:
            f.write(dict)
                
                
# Updates a dictionary with new key+values
def createJson(dict, id: str, chords: str, beats: float):
    s = {}
    s["chords"] = chords
    s["beats"] = beats
    dict[id] = s


# Compares two chord arrays based on matching indexes with their timestamp arrays
def compareChords(gt_timestamp, gt_chord, alg_timestamp, alg_chord):
    results = 0
    print(len(alg_timestamp))
    print(len(alg_chord))
    for idx, timestamp in enumerate(gt_timestamp):
        near = find_nearest(alg_timestamp, timestamp)
        algoChord = alg_chord[min(near, len(alg_chord)-1)]        # Preferrably better solution here
        print(timestamp)
        print(algoChord + " " + gt_chord[idx])
        if algoChord == gt_chord[idx]:
            results += 1
    # Return number of correct guesses divided by total guesses - can improve
    print(results)
    temp = results / len(gt_chord)
    return temp


# finds closest value in array
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def test(id):
    with open(dict.PROCESSED_JSON_PATH, 'r') as f:
        dataset = json.loads(f.read())
    beatRecognizer = beat_algorithm.BeatRecognizer(id)
    beatRecognizer.run()
    splitAudio(id, mode=dict.STEMS2, output=dict.ACCOMPANIMENT)
    resampleAudio(id, dict.SAMPLERATE_CHORDS)
    chords = chord_algorithm.chordHandler(id, beatRecognizer.beats)
    result = compareChords(dataset[id]["beats"], dataset[id]["chords"], beatRecognizer.beats, chords)
    print("The result is: " + str(result * 100) + chr(37) + " accuracy")
