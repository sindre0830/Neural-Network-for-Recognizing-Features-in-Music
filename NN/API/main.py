# import local modules
import dictionary as dict
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
