# import local modules
import dictionary as dict
import preprocessing
import beat_algorithm
import chord_algorithm
# import foreign modules
import flask
import time
import math
import warnings
import pandas

start_time = time.time()
app = flask.Flask(__name__)
# suppress warnings from Librosa
warnings.filterwarnings("ignore", category=Warning)


# Main program.
def main():
    # # define youtube id
    id = "qf9Ipqubh9g"
    # # parse songs.json if it exists for comparison data
    #preprocessing.parseJson(dict.JSON_PATH)
    # dict.printDivider()
    # # download file
    # preprocessing.downloadAudio(id)
    # # run beat recognizer
    # beatRecognizer = beat_algorithm.BeatRecognizer(id)
    # beatRecognizer.run(verbose=True)
    # # run chord recognizer
    # chordRecognizer = chord_algorithm.ChordRecognizer(id)
    # chordRecognizer.run(beats=beatRecognizer.beats, verbose=True)
    preprocessing.batchHandler()
    #preprocessing.test(id)
    #preprocessing.plotResults()



# Calculate time since program started in seconds.
def getUptime():
    return ("%i seconds" % math.floor(time.time() - start_time))


# Diagnosis endpoint.
@app.route(dict.DIAGNOSIS_PATH)
def diagnosis():
    output = {
        "Version": dict.VERSION,
        "Uptime": getUptime()
    }
    return output


# Analysis endpoint.
@app.route(dict.ANALYSIS_PATH)
def analysis():
    # get youtube id
    id = flask.request.args.get('id', None)
    if id is None:
        error = {
            "Msg": "Requires a YouTube ID, example: '.../v1/analysis?id=dQw4w9WgXcQ'"
        }
        return error, 404
    dict.printDivider()
    # preprocess audio file
    preprocessing.downloadAudio(id)
    # analyze song
    dict.printOperation("Run beat tracker...")
    beatRecognizer = beat_algorithm.BeatRecognizer(id)
    beatRecognizer.run()
    dict.printMessage(dict.DONE)
    dict.printOperation("Run chord tracker...")
    chordRecognizer = chord_algorithm.ChordRecognizer(id)
    chordRecognizer.run(beats=beatRecognizer.beats)
    dict.printMessage(dict.DONE)
    # return output
    output = {
        "bpm": beatRecognizer.bpm,
        "beats": beatRecognizer.beats.tolist(),
        "chords": chordRecognizer.chords.tolist()
    }
    return output


# branch if program is run through 'python main.py'
if __name__ == "__main__":
    main()
