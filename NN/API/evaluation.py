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
import keras
from pathlib import Path
from itertools import tee, islice, chain
from statistics import mean


# Object to perform chord tracking.
class Evaluators:
    # Temp algorithm data
    processed_beats: dict
    dataset: dict
    # Analysis results
    aggregate: dict
    new_chord_results: dict
    chord_results: dict
    new_beat_results: dict
    beat_results: dict
    detailed_results: dict

    class Evaluator:
        id: str
        chords: dict
        beats: dict

        def __init__(self, id: str):
            self.id = id

    def __init__(self):
        self.processed_beats = {}
        self.new_chord_results = {}
        self.chord_results = {}
        self.new_beat_results = {}
        self.beat_results = {}
        self.detailed_results = {}
        self.aggregate = {"chords": [], "beats": []}

    # Handles batch process comparison of database
    def batchHandler(self,
                     force: bool = False,
                     plot: bool = False,
                     verbose: bool = False,
                     model: keras.models.Sequential = None):

        # Validate existing data and prepare it
        self.checkData(force)

        # Iterate through dataset
        for id in self.dataset:
            if id in dict.BLACKLIST:
                pass
            else:
                if(verbose):
                    print(id)
                song = self.Evaluator(id)
                if id in self.chord_results.keys():
                    if(verbose):
                        print("Using saved result")
                    song.chords = self.compareChords(self.dataset[id]["beats"],
                                                     self.dataset[id]["chords"],
                                                     self.chord_results[id]["beats"],
                                                     self.chord_results[id]["chords"])
                    song.beats = self.beat_results[id]["beats"]
                # Get the data we need if not existing
                else:
                    if(verbose):
                        print("Generating from scratch...")
                    song.chords = self.processChords(id,
                                                     song,
                                                     self.dataset,
                                                     model)
                    song.beats = self.processBeats(self.dataset[id]["beats"], id)
                self.createJson(self.detailed_results,
                                id,
                                (song.chords, "chords"),
                                (song.beats, "beats"))
                self.aggregate["beats"].append(song.beats)
                self.aggregate["chords"].append(song.chords)
                if(verbose):
                    print("The result manual is: " + f'{song.chords:.2f}' + chr(37) + " chord accuracy, " +
                          f'{song.beats:.2f}' + chr(37) + " beat accuracy\n")
        # Write results
        self.output(plot)
        print("\n\tBatch evaluation complete!\n\n")

    # Handles beat recognition
    def processBeats(self,
                     id):
        beatRecognizer = beat_algorithm.BeatRecognizer(id)
        beatRecognizer.run()
        result = self.compareBeats(self.dataset, beatRecognizer.beats)
        preprocessing.deleteAudioFile(dict.getNativeAudioPath(id))
        self.createJson(self.new_beat_results,
                        id,
                        (result, "beats"))
        json_object = json.dumps(self.new_beat_results[id], indent=3)
        with open(dict.RESULTS_BEATS_PATH + id + '.json', "w+") as outfile:
            outfile.write(json_object)
        return result

    # Evaluate accuracy of beats
    def compareBeats(self,
                     algorithm: float,
                     verbose=False):
        beatAccuracy = []
        for previous, item, nxt in self.previous_and_next(self.dataset):
            nearIdx = self.find_nearest(algorithm, item)
            distance = item - algorithm[nearIdx]
            if nxt is None:
                nxt = previous
            if previous is None:
                previous = nxt
            if distance >= 0:
                control = abs(item - previous)
            else:
                control = abs(item - nxt)
            # We halve control - by default, it finds a value matching the previous control point
            # to be 0% accurate, even though it would be 100% accurate to that point
            beatAccuracy.append(100-abs((distance / (control/2))*100))
            if algorithm[nearIdx] == algorithm[-1]:
                break
        meanAccuracy = mean(beatAccuracy)
        if verbose:
            print("The average accuracy is: ", meanAccuracy)
        return meanAccuracy

    # Handles chord recognition
    def processChords(self,
                      id: str,
                      song: Evaluator,
                      model: keras.models.Sequential = None
                      ):
        preprocessing.downloadAudio(id)
        chordRecognizer = chord_algorithm.ChordRecognizer(id)
        song.beats = np.array(self.dataset[id]["beats"])
        # trim timestamps
        song.beats = song.beats[song.beats <= librosa.get_duration(filename=dict.getNativeAudioPath(id))]
        if model is None:
            chordRecognizer.run(beats=song.beats, solution="ALG", verbose=True)
        else:
            chordRecognizer.run(beats=song.beats, model=model, solution="CNN", verbose=True)

        result = self.compareChords(song.beats,
                                    self.dataset[id]["chords"],
                                    song.beats,
                                    chordRecognizer.chords)
        # Convert to %
        result = result*100
        # Save
        self.createJson(self.processed_beats,
                        id,
                        (self.dataset[id]["chords"], "chords"),
                        (song.beats.tolist(), "beats"))    # Update processed dataset

        self.createJson(self.new_chord_results,
                        id,
                        (chordRecognizer.chords.tolist(), "chords"),
                        (song.beats.tolist(), "fbeats"))
        json_object = json.dumps(self.new_chord_results[id], indent=3)
        with open(dict.RESULTS_SONG_PATH + id + '.json', "w+") as outfile:
            outfile.write(json_object)

        return result

    # Evaluate accuracy of chords - based on matching indexes with their timestamp arrays
    def compareChords(self,
                      gt_timestamp,
                      gt_chord,
                      alg_timestamp,
                      alg_chord):
        results = 0
        # We perform dictionary matching to ensure both chord lists
        # have chords in the same format
        alg_chord = [dict.algoFormat[k] for k in alg_chord]
        for idx, timestamp in enumerate(gt_timestamp):
            near = self.find_nearest(alg_timestamp,
                                     timestamp)
            algoChord = alg_chord[near]
            if algoChord == gt_chord[idx]:
                results += 1
        # Return number of correct guesses divided by total guesses - can improve
        temp = results / len(gt_chord)
        return temp*100

    # Updates a dictionary with new key+values
    def createJson(self,
                   dict,
                   id: str,
                   *variables):
        s = {}
        for variable in variables:
            s[variable[1]] = variable[0]
        dict[id] = s

    # records the results
    def output(self, plot: bool = False):

        # Update processed data with trimmed beats
        if(len(self.processed_beats)) > len(self.dataset):
            json_object = json.dumps(self.processed_beats,
                                     indent=3)
            with open(dict.PROCESSED_JSON_PATH, "w+") as outfile:
                outfile.write(json_object)

        # Write our new algorithm data to file
        if(len(self.new_chord_results)) > len(self.chord_results):
            print("Writing chord algorithm results...")
            json_object = json.dumps(self.new_chord_results,
                                     indent=3)
            with open(dict.CHORD_JSON_PATH, "w+") as outfile:
                outfile.write(json_object)

        if(len(self.new_beat_results)) > len(self.beat_results):
            print("Writing beat algorithm results...")
            json_object = json.dumps(self.new_beat_results,
                                     indent=3)
            with open(dict.BEAT_JSON_PATH, "w+") as outfile:
                outfile.write(json_object)

        json_object = json.dumps(self.detailed_results, indent=3)
        with open(dict.DETAILED_RESULTS_PATH, "w+") as outfile:
            outfile.write(json_object)

        # Plot if desired
        if plot:
            self.plotResults(False)

        # Generate CSV files with grouped accuracy
        df = pd.DataFrame(self.aggregate["chords"],
                          columns=['result'])   # get it in dataframe form
        aggregate = pd.cut(df['result'],
                           bins=pd.interval_range(start=0, end=100, periods=10)).value_counts()
        with open(dict.CHORDRESULTS_CSV_PATH, "w") as f:
            aggregate.to_csv(f)

        df = pd.DataFrame(self.aggregate["beats"], columns=['result'])
        aggregate = pd.cut(df['result'],
                           bins=pd.interval_range(start=0, end=100, periods=10)).value_counts()
        with open(dict.BEATRESULTS_CSV_PATH, "w") as f:
            aggregate.to_csv(f)

    # finds closest value in array
    def find_nearest(self,
                     array,
                     value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

    # Plot the beat or chord results into bins based on %accuracy
    def plotResults(self,
                    beat: bool = True):
        if beat:
            path = dict.BEATPLOT_PATH
            with open(dict.BEATRESULTS_CSV_PATH) as f:
                next(f)
                df = pd.read_csv(f, names=['range', 'number'])
                df = df.sort_values('range')
        else:
            path = dict.CHORDPLOT_PATH
            with open(dict.CHORDRESULTS_CSV_PATH) as f:
                next(f)
                df = pd.read_csv(f, names=['range', 'number'])
                df = df.sort_values('range')
        plt.bar(df['range'], df['number'], color='b')
        plt.title('Algorithm Accuracy')
        plt.xlabel("Accuracy %")
        plt.ylabel("# of songs")
        plt.xticks(rotation=25)
        plt.savefig(path)

    # updates json with new data from directory
    def updateJson(self,
                   file: str,
                   dir: str):
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
    def previous_and_next(self,
                          some_iterable):
        prevs, items, nexts = tee(some_iterable, 3)
        prevs = chain([None], prevs)
        nexts = chain(islice(nexts, 1, None), [None])
        return zip(prevs, items, nexts)

    def checkData(self, force: bool = False):
        # Make sure we have the dataset parsed
        if not os.path.exists(dict.PROCESSED_JSON_PATH) \
           or os.path.getsize(dict.PROCESSED_JSON_PATH) < os.path.getsize(dict.JSON_PATH) \
           or force:
            preprocessing.parseJson(dict.JSON_PATH)
        with open(dict.PROCESSED_JSON_PATH, 'r') as f:
            self.dataset = json.loads(f.read())

        # prep for results
        if not os.path.exists(dict.RESULTS_PATH):
            os.makedirs(dict.RESULTS_PATH)
        if not os.path.exists(dict.RESULTS_SONG_PATH):
            os.makedirs(dict.RESULTS_SONG_PATH)
        if not os.path.exists(dict.RESULTS_BEATS_PATH):
            os.makedirs(dict.RESULTS_BEATS_PATH)

        # Check if we have existing data for comparison and data does not need to be reprocessed
        if os.path.exists(dict.CHORD_JSON_PATH):
            algSize = os.path.getsize(dict.CHORD_JSON_PATH)
            if algSize != 0:
                if os.listdir(dict.RESULTS_SONG_PATH) != 0:
                    self.updateJson(dict.CHORD_JSON_PATH, dict.RESULTS_SONG_PATH)
                with open(dict.CHORD_JSON_PATH, 'r') as f:
                    self.chord_results = json.loads(f.read())

        if os.path.exists(dict.BEAT_JSON_PATH):
            algSize = os.path.getsize(dict.BEAT_JSON_PATH)
            if algSize != 0:
                if os.listdir(dict.RESULTS_BEATS_PATH) != 0:
                    self.updateJson(dict.BEAT_JSON_PATH, dict.RESULTS_BEATS_PATH)
                with open(dict.BEAT_JSON_PATH, 'r') as f:
                    self.beat_results = json.loads(f.read())
