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
    # preprocess audio file
    preprocessing.downloadAudio(id)
    preprocessing.splitAudio(id, mode=dict.NO_STEMS)
    preprocessing.resampleAudio(id, dict.SAMPLERATE_BEATS)
    # preprocessing.filterAudio(id)
    # analyze song
    _, librosaBeats = beat_algorithm.librosaBeatAnalysis(id)
    beat_algorithm.plotBeats(id, manual_beats=None, aubio_beats=None, librosa_beats=librosaBeats, start=None, end=None)
    preprocessing.splitAudio(id, mode=dict.STEMS4, output=dict.OTHER)
    preprocessing.resampleAudio(id, dict.SAMPLERATE_CHORDS)
    chord_algorithm.plotChromagram(id)


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
