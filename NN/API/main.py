import flask
import time
import math

start_time = time.time()

app = flask.Flask("NN-Internal-API")


def getUptime():
    return ("%i seconds" % math.floor(time.time() - start_time))


@app.route("/v1/diag")
def diagnosis():
    return {"Uptime": getUptime()}
