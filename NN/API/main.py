# import local modules
import dictionary as dict
import preprocessing
import beat_algorithm
import chord_algorithm
# import foreign modules
import flask
import time
import math

start_time = time.time()
app = flask.Flask(__name__)


# Main program.
def main():
    # define youtube id
    id = "N8BXtM6onEY"
    # preprocess audio file and perform beat tracking
    preprocessing.parseJson(dict.JSON_PATH)
    preprocessing.downloadAudio(id)
    preprocessing.splitAudio(id, mode=dict.NO_STEMS)
    preprocessing.resampleAudio(id, dict.SAMPLERATE_BEATS)
    _, librosaBeats = beat_algorithm.librosaBeatAnalysis(id)
    beat_algorithm.plotBeats(id, manual_beats=None, aubio_beats=None, librosa_beats=librosaBeats, start=None, end=None)
    # preprocess audio file and perform chord recognition
    preprocessing.splitAudio(id, mode=dict.STEMS2, output=dict.ACCOMPANIMENT)
    preprocessing.resampleAudio(id, dict.SAMPLERATE_CHORDS)
    chord_algorithm.getChord(id, librosaBeats[2], librosaBeats[3])


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
    # preprocess audio file
    preprocessing.downloadAudio(id)
    preprocessing.resampleAudio(id)
    # analyze song
    bpm, beats = beat_algorithm.librosaBeatAnalysis(id)
    # return output
    output = {
        "bpm": bpm,
        "beats": beats
    }
    return output


# branch if program is run through 'python main.py'
if __name__ == "__main__":
    main()
