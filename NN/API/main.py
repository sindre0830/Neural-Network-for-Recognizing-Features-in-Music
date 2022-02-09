import flask
import flask_restful

app = flask.Flask("NN-Internal-API")
api = flask_restful.Api(app)

class SongAnalysis(flask_restful.Resource):
    def get(self):
        youtubeID = flask.request.args.get(key="id")

        if youtubeID == None:
            return {"Message": "Error occured, requires a YouTube ID."}, 400

        return {"Message": youtubeID}, 200

api.add_resource(SongAnalysis, "/analyze")

app.run()
