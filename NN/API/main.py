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
    id = "dQw4w9WgXcQ"
    # preprocess audio file
    filename = preprocessing.downloadAudio(id)
    # analyze song
    beats, _ = beat_algorithm.analyseBeats(dict.AUDIO_DIR + filename)
    beat_algorithm.plotBeats(dict.AUDIO_DIR + filename, beats, start=3, end=4)


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
    filename = preprocessing.downloadAudio(id)
    # analyze song
    beats, bpm = beat_algorithm.analyseBeats(dict.AUDIO_DIR + filename)
    # return output
    output = {
        "bpm": bpm,
        "beats": beats
    }
    return output


# branch if program is run through 'python main.py'
if __name__ == "__main__":
    main()
