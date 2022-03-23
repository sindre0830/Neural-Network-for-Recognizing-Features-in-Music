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
import pandas as pd


# Downloads an audio file from given URL.
def downloadAudio(id):
    # branch if audio directory doesn't exist
    if not os.path.exists(dict.NATIVE_DIR):
        os.makedirs(dict.NATIVE_DIR)
    # branch if audio file doesn't exist
    if not os.path.isfile(dict.getNativeAudioPath(id)):
        # Try to download audio file with best quality then convert to wav
        os.system("yt-dlp -q -f 'ba' -x --audio-format wav https://www.youtube.com/watch?v=" + id + " -o '" + dict.NATIVE_DIR + "%(id)s.%(ext)s'")
        if not os.path.exists(dict.NATIVE_DIR + id + ".wav"):
            raise dict.YoutubeError



# Seperates instruments and vocals from audio file.
def splitAudio(id, mode, output=None):
    # branch if audio directory doesn't exist
    if not os.path.exists(dict.MODIFIED_DIR):
        os.makedirs(dict.MODIFIED_DIR)
    if mode is not dict.NO_STEMS:
        # split audio file according to the mode then move splitted file according to output
        os.system("spleeter separate -p spleeter:" + mode + " -o " + dict.MODIFIED_DIR + " " + dict.getNativeAudioPath(id) + " &> /dev/null")
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
    dict.printOperation("Parse songs.json for comparison data...")
    if os.path.exists(dict.JSON_PATH):
        dict.FLAG_DATABASE = True
        with open(path, 'r') as f:
            document = json.loads(f.read())

        current = {}
        if os.path.exists(dict.PROCESSED_JSON_PATH):
            with open(dict.PROCESSED_JSON_PATH, "r+") as f:
                if os.path.getsize(dict.PROCESSED_JSON_PATH) != 0:
                    current = json.loads(f.read())
        else:
            current = {}

        songs = {}

        for key in document:
            s = {}
            if key["youtubeLink"] not in dict.BLACKLIST:
                song = flattenSongData(key)
                s["chords"] = song["chords"]
                s["beats"] = song["beats"]
                songs[song["id"]] = s
        # Overwrite if new data
        if len(songs) > len(current):
            json_object = json.dumps(songs, indent=3)
            with open(dict.PROCESSED_JSON_PATH, "w+") as outfile:
                outfile.write(json_object)
        print(dict.SUCCESS)
    else:
        print(dict.FAILED)


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
            for chord in chords:
                length = chord["length"]
                if ("pause" in chord and chord["pause"]) or chord["chord"] == "pause":
                    for _ in range(int(length)):
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

    dataSize = os.path.getsize(dict.PROCESSED_JSON_PATH)
    with open(dict.PROCESSED_JSON_PATH, 'r') as f:
        dataset = json.loads(f.read())

    algSize = os.path.getsize(dict.ALGORITHM_JSON_PATH)

    # Check if we have existing data for comparison and data does not need to be reprocessed
    if (algSize == 0 or force):  # Add after debugging: or algSize != dataSize
        dict.FLAG_RESULTS = False
    else:
        dict.FLAG_RESULTS = True
        with open(dict.ALGORITHM_JSON_PATH, 'r') as f:
            results = json.loads(f.read())

    dictionary = {}
    # store our results
    batch_data = {}
    detailed_results = {}
    counter = 0
    # # Go through dataset
    for id in dataset:
        counter += 1
        print(id)
        # Get the data we need if not existing
        if not dict.FLAG_RESULTS:
            # try:
            #     downloadAudio(id)
            # except dict.YoutubeError:
            #     continue
            downloadAudio(id)
            beatRecognizer = beat_algorithm.BeatRecognizer(id)
            beatRecognizer.run()
            chordRecognizer = chord_algorithm.ChordRecognizer(id)
            temp = np.array(dataset[id]["beats"])
            chordRecognizer.run(beats=temp, verbose=True) #beatRecognizer.beats
            # Add to dictionary
            createJson(dictionary, id, chordRecognizer.chords, dataset[id]["beats"])
            result = compareChords(dataset[id]["beats"], dataset[id]["chords"], dataset[id]["beats"], chordRecognizer.chords)
        else:
            print("Entered else")
            result = compareChords(dataset[id]["beats"], dataset[id]["chords"], results[id]["beats"], results[id]["chords"])
        batch_data[id] = result*100
        createResults(detailed_results, id, algorithm = result)
        print("The result manual is: " + str(result * 100) + chr(37) + " accuracy")
        if not dict.FLAG_RESULTS:
            os.remove(dict.getNativeAudioPath(id))
            os.remove(dict.getModifiedAudioPath(id))
    output(batch_data, detailed_results)
    # Write our new algorithm data to file
    if not dict.FLAG_RESULTS:
        print("Writing algorithm results...")
        json_object = json.dumps(dictionary, indent=3)
        with open(dict.ALGORITHM_JSON_PATH, "w+") as outfile:
            outfile.write(json_object)


# Updates a dictionary with new key+values
def createJson(dict, id: str, chords: str, beats: float):
    s = {}
    s["chords"] = chords.tolist()
    s["beats"] = beats
    dict[id] = s


# Stores accuracy of Chord Algorithm and Neural Network for song
def createResults(dict, id: str, algorithm: float = None, neural: float = None):
    s = {}
    s["algo-accuracy"] = algorithm
    s["neural-accuracy"] = neural
    dict[id] = s


# Compares two chord arrays based on matching indexes with their timestamp arrays
def compareChords(gt_timestamp, gt_chord, alg_timestamp, alg_chord):
    results = 0
    for idx, timestamp in enumerate(gt_timestamp):
        near = find_nearest(alg_timestamp, timestamp)
        algoChord = alg_chord[near]        # Preferrably better solution here
        # print(timestamp)
        # print(algoChord + " " + gt_chord[idx])
        if algoChord == gt_chord[idx]:
            results += 1
    # Return number of correct guesses divided by total guesses - can improve
    #print(results)
    temp = results / len(gt_chord)
    return temp


# finds closest value in array
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


# records the batch processing results into CSV
def output(data, detailed):
    if not os.path.exists(dict.RESULTS_PATH):
        os.makedirs(dict.RESULTS_PATH)
    df = pd.DataFrame(list(data.items()), columns = ['id', 'result'])   # get it in dataframe form
    print(df.to_string())
    aggregate = pd.cut(df['result'], bins = pd.interval_range(start=0, end=100, periods=10)).value_counts()
    with open(dict.RESULTS_CSV_PATH, "w") as f:
        aggregate.to_csv(f)
    json_object = json.dumps(detailed, indent=3)
    with open(dict.DETAILED_RESULTS_PATH, "w+") as outfile:
        outfile.write(json_object)


def test(id):
    with open(dict.PROCESSED_JSON_PATH, 'r') as f:
        dataset = json.loads(f.read())
    downloadAudio(id)
    beatRecognizer = beat_algorithm.BeatRecognizer(id)
    beatRecognizer.run()
    chordRecognizer = chord_algorithm.ChordRecognizer(id)
    temp = np.array(dataset[id]["beats"])
    print(temp.shape)
    chordRecognizer.run(beats=temp, verbose=True)
    result1 = compareChords(dataset[id]["beats"], dataset[id]["chords"], dataset[id]["beats"], chordRecognizer.chords)
    print("The result is: " + str(result1 * 100) + chr(37) + " accuracy")
    os.remove(dict.getNativeAudioPath(id))
    os.remove(dict.getModifiedAudioPath(id))
