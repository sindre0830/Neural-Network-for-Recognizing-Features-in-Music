# import local modules
import dictionary as dict
import preprocessing
import beat_algorithm
import chord_algorithm
# import foreign modules
import os
import shutil
import librosa
import numpy as np
import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Handles batch process comparison of database
def batchHandler(force:bool = False, plot:bool = False):
    # Make sure we have the dataset parsed
    if not os.path.exists(dict.PROCESSED_JSON_PATH) or os.path.getsize(dict.PROCESSED_JSON_PATH) < 100:
        preprocessing.parseJson(dict.JSON_PATH)
    with open(dict.PROCESSED_JSON_PATH, 'r') as f:
        dataset = json.loads(f.read())

    # prep for results
    if not os.path.exists(dict.RESULTS_PATH):
        os.makedirs(dict.RESULTS_PATH)
    if not os.path.exists(dict.RESULTS_SONG_PATH):
        os.makedirs(dict.RESULTS_SONG_PATH)

    # Check if we have existing data for comparison and data does not need to be reprocessed
    updateJson(dict.ALGORITHM_JSON_PATH, dict.RESULTS_SONG_PATH)
    algSize = os.path.getsize(dict.ALGORITHM_JSON_PATH)
    if algSize != 0:  # Add after debugging: or algSize != dataSize
        with open(dict.ALGORITHM_JSON_PATH, 'r') as f:
            results = json.loads(f.read())
    else:
        results = {}

    dictionary = {}
    # store our results
    batch_data = {}
    detailed_results = {}
    # store updated songs
    newProcessed = {}
    songResults = {}
    # # Go through dataset
    for id in dataset:
        print(id)
        if id in results.keys():
            print("Using saved result")
            result = compareChords(dataset[id]["beats"], dataset[id]["chords"], dataset[id]["beats"], results[id]["chords"])       
        # Get the data we need if not existing
        else:
            print("Generating from scratch...")
            result = process(newProcessed, songResults)
        batch_data[id] = result*100
        createResults(detailed_results, id, algorithm = result)
        print("The result manual is: " + str(result * 100) + chr(37) + " accuracy")
    output(batch_data, detailed_results)
    # Update processed data with trimmed beats
    if(len(newProcessed)) > len(dataset):
        json_object = json.dumps(newProcessed, indent=3)
        with open(dict.PROCESSED_JSON_PATH, "w+") as outfile:
            outfile.write(json_object)
    # Write our new algorithm data to file
    if(len(songResults)) > len(results):
        print("Writing algorithm results...")
        json_object = json.dumps(dictionary, indent=3)
        with open(dict.ALGORITHM_JSON_PATH, "w+") as outfile:
            outfile.write(json_object)
    if plot:
        plotResults()


# Updates a dictionary with new key+values
def createJson(dict, id: str, first, second, fName:str, sName:str):
    s = {}
    s[fName] = first
    s[sName] = second
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
        algoChord = alg_chord[near]
        # print(timestamp)              # Debug
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


# Processes a song and stores the results
def process(newProcessed, songResults, dataset, dictionary):
    try:
        preprocessing.downloadAudio(id)
    except dict.YoutubeError:
        return
    chordRecognizer = chord_algorithm.ChordRecognizer(id)
    newBeats = np.array(dataset[id]["beats"])
    newBeats = newBeats[newBeats <= librosa.get_duration(filename=dict.getNativeAudioPath(id))]   # trim timestamps
    chordRecognizer.run(beats=newBeats, verbose=True)
    createJson(dictionary, id, chordRecognizer.chords.tolist(), newBeats.tolist(), "chords", "beats")
    result = compareChords(newBeats, dataset[id]["chords"], newBeats, chordRecognizer.chords)
    # Save
    createJson(newProcessed, id, dataset[id]["chords"], newBeats.tolist(), "chords", "beats")    # Update processed dataclear
    json_object = json.dumps(newProcessed[id], indent=3)
    with open(dict.TRIMMED_SONGS_PATH + id + '.json', "w+") as outfile:
        outfile.write(json_object)

    createJson(songResults, id, chordRecognizer.chords.tolist(), newBeats.tolist(), "chords", "beats")
    json_object = json.dumps(songResults[id], indent=3)
    with open(dict.RESULTS_SONG_PATH + id + '.json', "w+") as outfile:
        outfile.write(json_object)

    os.remove(dict.getNativeAudioPath(id))
    os.remove(dict.getModifiedAudioPath(id))
    return result


# records the batch processing results into CSV
def output(data, detailed):
    df = pd.DataFrame(list(data.items()), columns = ['id', 'result'])   # get it in dataframe form
    aggregate = pd.cut(df['result'], bins = pd.interval_range(start=0, end=100, periods=10)).value_counts()
    with open(dict.RESULTS_CSV_PATH, "w") as f:
        aggregate.to_csv(f)
    json_object = json.dumps(detailed, indent=3)
    with open(dict.DETAILED_RESULTS_PATH, "w+") as outfile:
        outfile.write(json_object)


# Plot the results into bins based on %accuracy
def plotResults():
    with open(dict.RESULTS_CSV_PATH) as f:
        next(f)
        df = pd.read_csv(f, names=['range', 'number'])
        df = df.sort_values('range')
    plt.bar(df['range'], df['number'], color = 'b')
    plt.title('Chord Algorithm Accuracy')
    plt.xlabel("Accuracy %")
    plt.ylabel("# of songs")
    plt.xticks(rotation=25)
    plt.savefig(dict.PLOT_PATH)


# updates json with new data from directory
def updateJson(file:str, dir:str):
    if os.path.getsize(file) == 0:
        resultsFile = {}
    else:
        with open(file, 'r') as f:
            resultsFile = json.loads(f.read())
    for f in os.listdir(dir):
        with open(dir + f, "rb") as infile:
            if Path(f).stem not in resultsFile:
                resultsFile[Path(f).stem] = json.load(infile)
    output = json.dumps(resultsFile, indent=3)
    with open(file, "w+") as outfile:
        outfile.write(output)
    shutil.rmtree(dir)