import flask
import flask_restful
import time
import math

start_time = time.time()

app = flask.Flask("NN-Internal-API")
api = flask_restful.Api(app)


def getUptime():
    return ("%i seconds" % math.floor(time.time() - start_time))


class Diagnosis(flask_restful.Resource):
    def get(self):
        return {"Uptime": getUptime()}, 200


api.add_resource(Diagnosis, "/v1/diag")

app.run()
