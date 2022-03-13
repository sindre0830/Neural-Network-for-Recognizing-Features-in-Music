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

start_time = time.time()
app = flask.Flask(__name__)
# suppress warnings from Librosa
warnings.filterwarnings("ignore", category=Warning)

# Main program.
def main():
    # parse songs.json if it exists for comparison data
    preprocessing.parseJson(dict.JSON_PATH)
    dict.printDivider()
    # define youtube id
    id = "N8BXtM6onEY"
    # download file
    preprocessing.downloadAudio(id)
    # run beat recognizer
    beatRecognizer = beat_algorithm.BeatRecognizer(id)
    beatRecognizer.run(verbose=True)
    # preprocess audio file and perform chord recognition
    preprocessing.splitAudio(id, mode=dict.STEMS2, output=dict.ACCOMPANIMENT)
    preprocessing.resampleAudio(id, dict.SAMPLERATE_CHORDS)
    chord_algorithm.getChord(id, beatRecognizer.beats[2], beatRecognizer.beats[3])


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
        return error
    dict.printDivider()
    # preprocess audio file
    preprocessing.downloadAudio(id)
    # analyze song
    dict.printOperation("Run beat tracker...")
    beatRecognizer = beat_algorithm.BeatRecognizer(id)
    beatRecognizer.run()
    dict.printMessage(dict.DONE)
    # return output
    output = {
        "bpm": beatRecognizer.bpm,
        "beats": beatRecognizer.beats.tolist()
    }
    return output


# branch if program is run through 'python main.py'
if __name__ == "__main__":
    main()
