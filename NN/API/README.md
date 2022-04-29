## Instructions

#### Docker

0. Download [Docker](https://docs.docker.com/get-docker/)
1. Run command ```docker build -t nn-internal .``` to build the image. Only needs to be done once
2. Run command ```docker run -p 5000:5000 nn-internal``` to start the container. Run this command anytime you would like to start the container again

To stop the container run the command ```docker ps``` to get the container id, then copy that id and run ```docker stop CONTAINER_ID```.

#### Manual (Linux)

0. Requires Python version 3.9
1. Run command ```apt-get update && apt-get -y install ffmpeg libsndfile1-dev``` to install dependencies for Spleeter
2. Run command ```pip install --no-deps -r requirements.txt``` to install required Python packages
3. Run command ```export FLASK_APP=main && flask run --host=0.0.0.0``` to run application

To stop the program press ```CTRL-C```

## Usage

1. Diag endpoint - *Used to get diagnostics of the API*
    - Input:
        ```
        Method: GET
        Path: .../diag
        ```
    - Output:
        ```json
        {
            "Uptime": string,
            "Version": string
        }
        ```
    - Example:
        - Input:
            ```
            Method: GET
            Path: http://localhost:5000/v1/diag
            ```
        - Output:
            ```json
            {
                "Uptime": "1791 seconds",
                "Version": "v1"
            }
            ```

2. Analysis endpoint - *Used to get analysis of song on youtube*
    - Input:
        ```
        Method: GET
        Path: .../analysis{?id=youtube_id}
        ```
        - Endpoint will return an error if the youtube_id parameter isn't added.
    - Output:
        ```json
        {
            "beats": [float],
            "bpm": float,
            "chords": [string]
        }
        ```
    - Example:
        - Input:
            ```
            Method: GET
            Path: http://localhost:5000/v1/analysis?id=dQw4w9WgXcQ
            ```
        - Output:
            ```json
            {
                "beats": [
                    0.1536,
                    0.6144,
                    1.1264,
                    ...
                    209.0496
                ],
                "bpm": 117.1875,
                "chords": [
                    "A",
                    "E",
                    "F#m",
                    ...
                    "A#m"
                ]
            }
            ```
