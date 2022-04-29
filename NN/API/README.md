# Instructions

### Docker

0. Download [Docker](https://docs.docker.com/get-docker/)
1. Run command ```docker build -t nn-internal .``` to build image. Only needs to be done once
2. Run command ```docker run -p 5000:5000 nn-internal``` to run container. Run this command anytime you would like to start the container again

To stop the container run the command ```docker ps``` to get the container id, then copy that id and run ```docker stop CONTAINER_ID```.

### Manual (Linux)

0. Requires Python version 3.9
1. Run command ```apt-get update && apt-get -y install ffmpeg libsndfile1-dev``` to install dependencies for Spleeter
2. Run command ```pip install --no-deps -r requirements.txt``` to install required Python packages
3. Run command ```export FLASK_APP=main && flask run --host=0.0.0.0``` to run application

To stop the program press ```CTRL-C```
