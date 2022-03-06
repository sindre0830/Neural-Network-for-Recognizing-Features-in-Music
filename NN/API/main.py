# import local modules
import dictionary as dict
import preprocessing
import beat_algorithm
# import foreign modules
import flask
import time
import math

start_time = time.time()
app = flask.Flask(__name__)


# Main program.
def main():
    # define youtube id
    id = "EX7oWSbVbGY"
    # preprocess audio file
    preprocessing.downloadAudio(id)
    # analyze song
    _, aubioBeats = beat_algorithm.aubioBeatAnalysis(id)
    _, librosaBeats = beat_algorithm.librosaBeatAnalysis(id)
    beat_algorithm.plotBeats(id, manual_beats=None, aubio_beats=aubioBeats, librosa_beats=librosaBeats, start=0, end=10)


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
