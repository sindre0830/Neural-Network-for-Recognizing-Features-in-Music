## Instructions
You need to create a serviceAccountKey.json file and add the service key provided by your [firebase project](https://firebase.google.com/docs/admin/setup#initialize-sdk) to this file.

#### Docker
0. Download [Docker](https://docs.docker.com/get-docker/)
1. Run the command ```docker build -t main-api .``` to build the image. Only needs to be done once
2. Run the command ```docker run --network="host" -p 8080:8080 main-api``` to build and run the container.
    - To stop the container run the command ```docker ps``` to get the container id, then copy that id and run ```docker stop CONTAINER_ID```
    - To start the container again, run the command ```docker ps -a``` to get the container id, then copy that id and run ```docker start CONTAINER_ID```

#### Manual (Linux)
0. Uses Golang version 1.17
1. Run the command ```go build ./main.go``` to build the application.
2. Run the command ```./main``` to start the program.
    - To stop the program press ```CTRL-C```

## Usage
Root path: http://localhost:8080/v1/

1. Analysis endpoint - *Used to send songs to analysis*
    - Input:
        ```
        Method: POST
        Path: .../analysis{?id=youtube_id}
        Body:
            {
                "link": string
            }
        ```
    - Output:
        ```If the request is successful, nothing will be returned```
    - Example:
        - Input:
            ```
            Method: POST
            Path: http://localhost:8080/v1/analysis
            Body:
                {
                    "link": "https://www.youtube.com/watch?v=szeXkBYq5HU"
                }
2. Diag endpoint - *Used to get diagnostics of the API*
    - Input:
        ```
        Method: GET
        Path: .../diag
        ```
    - Output:
        ```
        {
            "model_connection": int,
            "processing_songs": [string],
            "failed_songs": [string]
        }
    - Example:
        - Input:
            ```
            Method: GET
            Path: http://localhost:8080/v1/diag
            ```
        - Output:
            ```json
            {
                "model_connection": 200,
                "failed_songs": [
                    "6mGpRsC-8eU",
                    "7ZYgKCbFbWY"
                ],
                "processing_songs": [
                    "O4irXQhgMqg"
                ]
            }
            ```
3. Results endpoint - *Used to retrieve and update results*
    
    3.1 Retrieving results
    - Input:
        ```
        Method: GET
        Path: .../results
        ```
    - Output:
        ```
        {
            [
                {
                    "approved": bool,
                    "beats": [float],
                    "bpm": float,
                    "chords": [string],
                    "failed": bool,
                    "processing": bool,
                    "title": string,
                    "id": string
                }
            ]
        }
        ```
    - Example:
        - Input:
            ```
            Method: GET
            Path: localhost:8080/v1/results
            ```
        - Output:
            ```json
            {
                [
                    {
                        "approved": true,
                        "beats": [
                            0.2425,
                            1.3414,
                            ...
                            120.4124
                        ],
                        "bpm": 142.4214,
                        "chords": [
                            "A",
                            "E",
                            ...
                            "A#m"
                        ],
                        "failed": false,
                        "processing": false,
                        "title": "The The - This Is the Day (Official Audio)",
                        "id": "7ZYgKCbFbWY"
                    },
                    ...
                ]
            }
            ```
    3.2 Deleting result
    - Input:
        ```
        Method: DELETE
        Path: .../results{?id=youtube_id}
        ```
    - Output:
        ```If the request is successful, nothing will be returned```
    - Example:
        - Input:
            ```
            Method: DELETE
            Path: http://localhost:8080/results?id=mdJDPepGOAM
            ```
    3.3 Updating result
    - Input:
        ```
        Method: PUT
        Path: .../results{?id=youtube_id}
        Body:
            {
                "title": string,
                "bpm": float,
                "beats": [float],
                "chords": [string]
            }
        ```
        - The body must contain at least 1 of the fields listed in body, and might contain more.
    - Output:
        ```If the request is successful, nothing will be returned```
    - Example:
        - Input:
            ```
            Method: PUT
            Path: http://localhost:8080/results?id=19xq47SVrnw
            Body:
                {
                    "bpm": 134.2341,
                    "chords": [
                        "A",
                        "C",
                        ...
                        "F#"
                    ] 
                }
            ```

