# import local modules
from preprocessing import (
    loadDataset,
    prepareDataset
)
# import foreign modules
import os
import tensorflow as tf

# suppress info and warnings outputted by tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
# enable memory growth for gpu devices
# source: https://stackoverflow.com/a/55541385/8849692
gpu_devices = tf.config.experimental.list_physical_devices('GPU')
if gpu_devices:
    for device in gpu_devices:
        tf.config.experimental.set_memory_growth(device, True)


# Main program.
def main():
    # load dataset from file and process it to correct type
    data, labels = loadDataset()
    data, labels = prepareDataset(data, labels)


# branch if program is run through 'python main.py' and run main program
if __name__ == "__main__":
    main()
