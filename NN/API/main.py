# import local modules
import dictionary as dict
import preprocessing
import beat_algorithm
import chord_algorithm
# import foreign modules
import flask
import time
import math
import warnings
import os
import tensorflow as tf
import keras
import http

start_time = time.time()
app = flask.Flask(__name__)
# suppress warnings from Librosa
warnings.filterwarnings("ignore", category=Warning)
# suppress info and warnings outputted by tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
# enable memory growth for gpu devices
# source: https://stackoverflow.com/a/55541385/8849692
gpu_devices = tf.config.experimental.list_physical_devices('GPU')
if gpu_devices:
    for device in gpu_devices:
        tf.config.experimental.set_memory_growth(device, True)
# load model once
modelChord = keras.models.load_model(dict.MODEL_PATH)


# Main program.
def main():
    # parse songs.json if it exists for comparison data
    preprocessing.parseJson(dict.JSON_PATH)
    dict.printDivider()
    # define youtube id
    id = "GudvNP9AwNM"
    # download file
    preprocessing.downloadAudio(id)
    # run beat recognizer
    beatRecognizer = beat_algorithm.BeatRecognizer(id)
    beatRecognizer.run(plot=True, verbose=True)
    # run chord recognizer
    chordRecognizer = chord_algorithm.ChordRecognizer(id)
    chordRecognizer.run(beats=beatRecognizer.beats, model=modelChord, verbose=True)
    print(chordRecognizer.chords)


# Calculate time since program started in seconds.
def getUptime():
    return ("%i seconds" % math.floor(time.time() - start_time))


# Diagnosis endpoint.
@app.route(dict.DIAGNOSIS_ENDPOINT)
def diagnosis():
    output = {
        "version": dict.VERSION,
        "uptime": getUptime()
    }
    return output, http.HTTPStatus.OK


# Analysis endpoint.
@app.route(dict.ANALYSIS_ENDPOINT)
def analysis():
    # get youtube id
    id = flask.request.args.get('id', None)
    if id is None:
        error = {
            "msg": "Requires a YouTube ID, example: '.../v1/analysis?id=dQw4w9WgXcQ'"
        }
        return error, http.HTTPStatus.BAD_REQUEST
    # preprocess audio file
    preprocessing.downloadAudio(id)
    # analyze song
    beatRecognizer = beat_algorithm.BeatRecognizer(id)
    beatRecognizer.run()
    chordRecognizer = chord_algorithm.ChordRecognizer(id)
    chordRecognizer.run(beats=beatRecognizer.beats, model=modelChord)
    # return output
    output = {
        "bpm": beatRecognizer.bpm,
        "beats": beatRecognizer.beats.tolist(),
        "chords": chordRecognizer.chords.tolist()
    }
    return output, http.HTTPStatus.OK


# Clean-up endpoint.
@app.route(dict.REMOVE_ENDPOINT)
def remove():
    # get youtube id
    id = flask.request.args.get('id', None)
    if id is None:
        error = {
            "msg": "Requires a YouTube ID, example: '.../v1/remove?id=dQw4w9WgXcQ'"
        }
        return error, http.HTTPStatus.BAD_REQUEST
    # remove audio file
    preprocessing.deleteAudioFile(dict.getNativeAudioPath(id))
    # return output
    output = ''
    return output, http.HTTPStatus.OK


# branch if program is run through 'python main.py'
if __name__ == "__main__":
    main()
