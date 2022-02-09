import flask
import flask_restful

app = flask.Flask("NN-Internal-API")
api = flask_restful.Api(app)

class SongAnalysis(flask_restful.Resource):
    # methods...
    pass

api.add_resource(SongAnalysis, "/analyze")
