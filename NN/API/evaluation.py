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
from itertools import tee, islice, chain
from statistics import mean


# Object to perform chord tracking.
class Evaluators:
    # Store algorithm data - make one variable
    processed_beats:dict # Don't need?
    beat_chord_aggregate:dict # Don't need?
    song_buffer:dict # Don't need?
    # Analysis results  
    results:dict
    detailed_results:dict
    
    class Evaluator:
        id: str
        chords: dict
        beats: dict
        
        def __init__(self, id: str):
            self.id = id
    
    def __init__(self):
        self.processed_beats = {} # Don't need?
        self.beat_chord_aggregate = {} # Don't need?
        self.song_buffer = {} # Don't need?
        self.results = {}
        self.detailed_results = {}


    # Handles batch process comparison of database
    def batchHandler(self, force:bool = False, plot:bool = False):
        # Make sure we have the dataset parsed - CHANGE
        if not os.path.exists(dict.PROCESSED_JSON_PATH) or os.path.getsize(dict.PROCESSED_JSON_PATH) < os.path.getsize(dict.JSON_PATH):
            preprocessing.parseJson(dict.JSON_PATH)
        with open(dict.PROCESSED_JSON_PATH, 'r') as f:
            dataset = json.loads(f.read())

        # prep for results
        if not os.path.exists(dict.RESULTS_PATH):
            os.makedirs(dict.RESULTS_PATH)
        if not os.path.exists(dict.RESULTS_SONG_PATH):
            os.makedirs(dict.RESULTS_SONG_PATH)

        # Check if we have existing data for comparison and data does not need to be reprocessed
        if os.path.exists(dict.ALGORITHM_JSON_PATH):
            algSize = os.path.getsize(dict.ALGORITHM_JSON_PATH) 
            if algSize != 0:
                if os.listdir(dict.RESULTS_SONG_PATH) != 0:
                    updateJson(dict.ALGORITHM_JSON_PATH, dict.RESULTS_SONG_PATH)
                with open(dict.ALGORITHM_JSON_PATH, 'r') as f:
                    results = json.loads(f.read())
        else:
            results ={}

        # # Go through dataset
        for id in dataset:
            if id in dict.BLACKLIST:
                pass
            else:
                print(id)
                song = self.Evaluator(id)
                if id in results.keys():
                    print("Using saved result")
                    song.chords = self.compareChords(dataset[id]["beats"], dataset[id]["chords"], results[id]["beats"], results[id]["chords"])
                    song.beats = results[id]["beats"]
                # Get the data we need if not existing
                else:
                    print("Generating from scratch...")
                    song.chords = self.processChords(id, song, dataset)
                    meanbeat, song.beats = self.processBeats(dataset[id]["beats"], id)
                self.createResults(self.detailed_results, id, algorithm = song.chords)
                print("The result manual is: " + str(song.chords * 100) + chr(37) + " accuracy")
        
        # Update processed data with trimmed beats
        if(len(self.processed_beats)) > len(dataset):
            json_object = json.dumps(self.processed_beats, indent=3)
            with open(dict.PROCESSED_JSON_PATH, "w+") as outfile:
                outfile.write(json_object)
        # Write our new algorithm data to file
        if(len(self.song_buffer)) > len(results):
            print("Writing algorithm results...")
            json_object = json.dumps(self.beat_chord_aggregate, indent=3)
            with open(dict.ALGORITHM_JSON_PATH, "w+") as outfile:
                outfile.write(json_object)
        if plot:
            plotChordResults()
            
            # TEST THIS ONE
    # Processes a song and stores the results
    def processChords(self, id: str, song:Evaluator, dataset):
        try:
            preprocessing.downloadAudio(id)
        except dict.YoutubeError:
            return
        chordRecognizer = chord_algorithm.ChordRecognizer(id)
        song.beats = np.array(dataset[id]["beats"])
        song.beats = song.beats[song.beats <= librosa.get_duration(filename=dict.getNativeAudioPath(id))]   # trim timestamps
        chordRecognizer.run(beats=song.beats, solution="ALG", verbose=True)
        self.createJson(self.beat_chord_aggregate, id, chordRecognizer.chords.tolist(), song.beats.tolist(), "chords", "beats")
        result = self.compareChords(song.beats, dataset[id]["chords"], song.beats, chordRecognizer.chords)
        # Save
        self.createJson(self.processed_beats, id, dataset[id]["chords"], song.beats.tolist(), "chords", "beats")    # Update processed dataclear
        json_object = json.dumps(self.processed_beats[id], indent=3)
        with open(dict.TRIMMED_SONGS_PATH + id + '.json', "w+") as outfile:
            outfile.write(json_object)

        self.createJson(self.song_buffer, id, chordRecognizer.chords.tolist(), song.beats.tolist(), "chords", "beats")
        json_object = json.dumps(self.song_buffer[id], indent=3)
        with open(dict.RESULTS_SONG_PATH + id + '.json', "w+") as outfile:
            outfile.write(json_object)

        return result

    # Updates a dictionary with new key+values
    def createJson(self, dict, id: str, first, second, fName:str, sName:str):
        s = {}
        s[fName] = first
        s[sName] = second
        dict[id] = s


    # Stores accuracy of Chord Algorithm and Neural Network for song
    def createResults(self, dict, id: str, algorithm: float = None, neural: float = None):
        s = {}
        s["algo-accuracy"] = algorithm
        s["neural-accuracy"] = neural
        dict[id] = s


    # Compares two chord arrays based on matching indexes with their timestamp arrays
    def compareChords(self, gt_timestamp, gt_chord, alg_timestamp, alg_chord):
        results = 0
        for idx, timestamp in enumerate(gt_timestamp):
            near = find_nearest(alg_timestamp, timestamp)
            algoChord = alg_chord[near]
            # print(timestamp)              # Debug
            # print(algoChord + " " + gt_chord[idx])
            if algoChord == gt_chord[idx]:
                results += 1
        # Return number of correct guesses divided by total guesses - can improve
        temp = results / len(gt_chord)
        return temp


    # records the batch processing results into CSV
    def output(self, chorddata = None, beatdata = None, detailed = None):
        if chorddata:
            df = pd.DataFrame(list(chorddata.items()), columns = ['id', 'result'])   # get it in dataframe form
            aggregate = pd.cut(df['result'], bins = pd.interval_range(start=0, end=100, periods=10)).value_counts()
            with open(dict.CHORDRESULTS_CSV_PATH, "w") as f:
                aggregate.to_csv(f)
        if detailed:
            json_object = json.dumps(detailed, indent=3)
            with open(dict.DETAILED_RESULTS_PATH, "w+") as outfile:
                outfile.write(json_object)
        if beatdata:
            df = pd.DataFrame(list(beatdata.items()), columns = ['id', 'result'])
            #print(df)
            aggregate = pd.cut(df['result'].str['accuracy'], bins = pd.interval_range(start=0, end=100, periods=10)).value_counts()
            with open(dict.BEATRESULTS_CSV_PATH, "w") as f:
                aggregate.to_csv(f)



    def processBeats(self, dataset, id):
        beatRecognizer = beat_algorithm.BeatRecognizer(id)
        beatRecognizer.run()
        os.remove(dict.getNativeAudioPath(id))  # Clear up audio data
        return self.evaluateBeats(dataset, beatRecognizer.beats)


    def evaluateBeats(self, dataset:float, algorithm:float, verbose = False):
        beatAccuracy = []
        for previous, item, nxt in previous_and_next(dataset):
            nearIdx = find_nearest(algorithm, item)
            distance = item - algorithm[nearIdx]
            if nxt == None:
                nxt = previous
            if previous == None:
                previous = nxt
            if distance >= 0:
                control = abs(item - previous)
            else:
                control = abs(item - nxt)
            # We halve control - at normal, it finds a value matching the control point
            # to be 0% accurate, even though it's 100% accurate to the control.
            beatAccuracy.append(100-abs((distance / (control/2))*100))
            if algorithm[nearIdx] == algorithm[-1]:  # Indicates dataset is longer
                break
        meanAccuracy = mean(beatAccuracy)
        if verbose:
            print("The average accuracy is: ", meanAccuracy)
        return meanAccuracy, beatAccuracy


    def beatProcess(self, force:bool = False, verbose:bool = False):
        with open(dict.PROCESSED_JSON_PATH, 'r') as f:
            dataset = json.loads(f.read())
        if not os.path.exists(dict.RESULTS_BEATS_PATH):
            os.makedirs(dict.RESULTS_BEATS_PATH)
        beat_data = {}
        updateJson(dict.BEAT_RESULTS_PATH, dict.RESULTS_BEATS_PATH) # avoid error on nonexistent file here
        beatSize = os.path.getsize(dict.BEAT_RESULTS_PATH)
        if beatSize != 0:
            with open(dict.BEAT_RESULTS_PATH, 'r') as f:
                results = json.loads(f.read())
        else:
            results = {}

        for id in dataset:
            if id not in results.keys() or force:
                print("Evaluating beats for id: " + id)
                try:
                    preprocessing.downloadAudio(id)
                except dict.YoutubeError:
                    return    
                beatRecognizer = beat_algorithm.BeatRecognizer(id)
                beatRecognizer.run()
                accuracy, beatresults = self.evaluateBeats(dataset[id]["beats"], beatRecognizer.beats)
                self.createJson(beat_data, id, accuracy, beatresults, "accuracy", "beat_results")
                json_object = json.dumps(beat_data[id], indent=3)
                with open(dict.RESULTS_BEATS_PATH + id + '.json', "w+") as outfile:
                    outfile.write(json_object)
                os.remove(dict.getNativeAudioPath(id))
                os.remove(dict.getModifiedAudioPath(id))
            else:
                print("Data already exists for " + id + ", skipping to next...")
        self.output(chorddata=None, beatdata=results, detailed=None)
        if verbose:
            plotBeatResults()
            with open(dict.BEAT_RESULTS_PATH, 'r') as f:
                printing = json.loads(f.read())
            df = pd.DataFrame.from_dict(printing)
            df['average'] = df[:1].mean(axis=1)
            print("Average accuracy: " + str(df['average']['accuracy']))


# finds closest value in array
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


# Plot the results into bins based on %accuracy
def plotChordResults():
    with open(dict.CHORDRESULTS_CSV_PATH) as f:
        next(f)
        df = pd.read_csv(f, names=['range', 'number'])
        df = df.sort_values('range')
    plt.bar(df['range'], df['number'], color = 'b')
    plt.title('Algorithm Accuracy')
    plt.xlabel("Accuracy %")
    plt.ylabel("# of songs")
    plt.xticks(rotation=25)
    plt.savefig(dict.CHORDPLOT_PATH)


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
    os.makedirs(dir)


# Source: https://stackoverflow.com/a/1012089
# Takes an iterable and returns list of 3-element tuples that lets us
# access the previous and next element for each item
# Used to compare distances between chords for the beat dataset
def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(prevs, items, nexts)


def plotBeatResults():
    with open(dict.BEATRESULTS_CSV_PATH) as f:
        next(f)
        df = pd.read_csv(f, names=['range', 'number'])
        df = df.sort_values('range')
    plt.bar(df['range'], df['number'], color = 'b')
    plt.title('Algorithm Accuracy')
    plt.xlabel("Accuracy %")
    plt.ylabel("# of songs")
    plt.xticks(rotation=25)
    plt.savefig(dict.BEATPLOT_PATH)