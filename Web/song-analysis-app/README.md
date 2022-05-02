## Instructions
#### Docker
0. Download [Docker](https://docs.docker.com/get-docker/)
1. Run the command ```docker build -t song-analysis .``` to build the image. Only needs to be done once
2. Run the command ```docker run --network="host" -p 3000:3000 song-analysis``` to build and run the container.
    - To stop the container run the command ```docker ps``` to get the container id, then copy that id and run ```docker stop CONTAINER_ID```
    - To start the container again, run the command ```docker ps -a``` to get the container id, then copy that id and run ```docker start CONTAINER_ID```

### Manual
1. Run the command ```npm install```
2. Run the command ```npm start```
  - To stop the program press ```CTRL-C```

## Tests
1. Run the command ```npm test```

All test files are in the folder of the component they belong to.
