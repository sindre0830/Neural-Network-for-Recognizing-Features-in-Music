# import local modules
import dictionary as dict
# import foreign modules
import os
import librosa
import soundfile as sf
import shutil
import numpy as np
import json


# Downloads an audio file from given URL.
def downloadAudio(id: str):
    # branch if audio directory doesn't exist
    if not os.path.exists(dict.NATIVE_DIR):
        os.makedirs(dict.NATIVE_DIR)
    # branch if audio file doesn't exist
    if not os.path.isfile(dict.getNativeAudioPath(id)):
        # download audio file with best quality then convert to wav
        os.system("yt-dlp -q -f 'ba' -x --audio-format wav https://www.youtube.com/watch?v=" + id + " -o '" + dict.NATIVE_DIR + "%(id)s.%(ext)s'")


# Seperates instruments and vocals from audio file.
def splitAudio(id: str, mode: str, output:str = None):
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
def resampleAudio(id: str, samplerate: int):
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
def filterAudio(id: str):
    y, sr = librosa.load(path=dict.getModifiedAudioPath(id), sr=None)
    applyFilter = np.vectorize(lambda t: 0. if t < 0.15 else t)
    y = applyFilter(y)
    sf.write(dict.getModifiedAudioPath(id), data=y, samplerate=sr)


# Delete modified audio file.
def deleteModifiedAudio(id: str):
    if os.path.exists(dict.getModifiedAudioPath(id)):
        os.remove(dict.getModifiedAudioPath(id))


# Parses songs.json to a simplified JSON object.
def parseJson(path: str):
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

    char = chr(charNum + 65)

    if chordNum == 1 or chordNum == 4 or chordNum == 6 or chordNum == 9 or chordNum == 11:
        char += "#"

    if minor:
        char += "m"

    return char


# generate training set for NN training through songs.json (provided by EC-Play).
def getTrainingData():
    data = []
    label = []
    maxLength = 0
    a = 0
    # load parsed JSON file
    with open(dict.PROCESSED_JSON_PATH, 'r') as f:
        ECPlayDataset = json.loads(f.read())
    # iterate through each song
    for key in ECPlayDataset:
        a += 1
        # preprocess audio file
        downloadAudio(key)
        splitAudio(key, mode=dict.STEMS2, output=dict.ACCOMPANIMENT)
        resampleAudio(key, dict.SAMPLERATE_CHORDS)
        beats = ECPlayDataset[key]["beats"]
        chords = ECPlayDataset[key]["chords"]
        # iterate through each beat in song
        for i in range(len(beats)):
            # branch if beat is not last and its not a pause
            if i + 1 < len(beats) and chords[i] != '':
                # try to convert audio sample to chromagram and add to list, otherwise skip to next song
                chroma, maxLength = getChordChroma(key, maxLength, start=beats[i], end=beats[i + 1])
                if chroma is not None:
                    data.append(chroma)
                    label.append(chords[i])
                else:
                    break
        print(str(a) + "\t" + key + "\tlength: " + str(len(data)) + "\tmax_lenght: " + str(maxLength))
    # extend each chromagram to the largest length found
    for i in range(len(data)):
        data[i] = extendMatrix(data[i], maxLength)
        # print info if an error occurred
        if maxLength != data[i].shape[1]:
            print("index: " + str(i) + "\tlength: " + str(data[i].shape[1]) + "\tmax_length: " + str(maxLength))
    # compact data and label to tuple and save to file
    dataset = (data, label)
    dataset = np.array(dataset)
    # branch if audio directory doesn't exist
    if not os.path.exists(dict.TRAINING_DATASET_PATH):
        os.makedirs(dict.TRAINING_DATASET_PATH)
    np.save(dict.TRAINING_DATASET_PATH + "dataset.npy", dataset)


# Generate chromagram from audio sample.
def getChordChroma(id: str, max_length: int, start: float, end: float):
    # load audio sample and branch if it was able to load the audio sample
    y, sr = librosa.load(dict.getModifiedAudioPath(id), sr=None, offset=start, duration=(end - start))
    if np.any(y):
        # generate chromagram and branch if there is enough data (threshold set to 10 data points)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        if np.any(chroma) and chroma.shape[1] > 10:
            if chroma.shape[1] > max_length:
                max_length = chroma.shape[1]
            return chroma, max_length
    return None, max_length


# Extend matrix on the X axis by n length evenly.
def extendMatrix(mat: np.ndarray, max_length: int):
    INIT_LENGTH = mat.shape[1]
    if INIT_LENGTH == max_length:
        return mat
    length = INIT_LENGTH
    max_length -= INIT_LENGTH
    double = max_length // INIT_LENGTH
    rest = max_length - (double * INIT_LENGTH)
    # double the size of the matrix
    for i in range(double):
        length += INIT_LENGTH
        for j in range(length):
            if j % (i + 2) != 0:
                continue
            mat = np.insert(mat, j + i + 1, mat[:, j + i], axis=1)
    if rest == 0:
        return mat
    # apply the rest evenly
    skip = length / rest
    total = 0
    i = 0
    j = 0
    while j < length:
        if j > total:
            mat = np.insert(mat, i + 1, mat[:, i], axis=1)
            total += skip
            i += 1
        i += 1
        j += 1
    return mat
