import flask
import flask_restful

app = flask.Flask("NN-Internal-API")
api = flask_restful.Api(app)


class Diagnosis(flask_restful.Resource):
    def get(self):
        return {}, 200


api.add_resource(Diagnosis, "/v1/diag")

app.run()
