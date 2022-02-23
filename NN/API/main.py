# import local modules
import dictionary as dict
import preprocessing
# import foreign modules
import flask
import time
import math

start_time = time.time()
app = flask.Flask(__name__)


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
            "Msg": "Requires a YouTube ID like this '.../v1/analysis?id=dQw4w9WgXcQ'"
        }
        return error
    # preprocess audio file
    preprocessing.downloadAudio(id)
    # return output
    output = {
        "id": id
    }
    return output
