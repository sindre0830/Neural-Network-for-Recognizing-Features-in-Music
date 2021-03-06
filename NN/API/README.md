## Instructions
#### Docker
0. Download [Docker](https://docs.docker.com/get-docker/)
1. Run the command ```docker build -t main-api .``` to build the image. Only needs to be done once
2. Run the command ```docker run --network="host" -p 8080:8080 main-api``` to build and run the container.
    - To stop the container run the command ```docker ps``` to get the container id, then copy that id and run ```docker stop CONTAINER_ID```
    - To start the container again, run the command ```docker ps -a``` to get the container id, then copy that id and run ```docker start CONTAINER_ID```

#### Manual (Linux)
0. Requires Python version 3.9
1. Run the command ```apt-get update && apt-get -y install ffmpeg libsndfile1-dev``` to install dependencies for Spleeter
2. Run the command ```pip install --no-deps -r requirements.txt``` to install required Python packages
3. Run the command ```export FLASK_APP=main && flask run --host=0.0.0.0``` to start the program
    - To stop the program press ```CTRL-C```

## Usage
Root path: http://localhost:5000/v1/

1. Diag endpoint - *Used to get diagnostics of the API*
    - Input:
        ```
        Method: GET
        Path: .../diag
        ```
    - Output:
        ```
        {
            "uptime": string,
            "version": string
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
                "uptime": "1791 seconds",
                "version": "v1"
            }
            ```
2. Analysis endpoint - *Used to get analysis of song on youtube*
    - Input:
        ```
        Method: GET
        Path: .../analysis{?id=youtube_id}
        ```
        - Endpoint will return an error if the youtube_id parameter isn't added. *See error handling below*
    - Output:
        ```
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
3. Remove endpoint - *Used to remove cached audio files after running analysis endpoint*
    - Input:
        ```
        Method: GET
        Path: .../remove{?id=youtube_id}
        ```
        - Endpoint will return an error if the youtube_id parameter isn't added. *See error handling below*
    - Output:
        ```If the request is successful, nothing will be returned```
    - Example:
        - Input:
            ```
            Method: GET
            Path: http://localhost:5000/v1/remove?id=dQw4w9WgXcQ
            ```

## Error Handling
If the analysis or the remove endpoint doesn't have the ```id``` parameter, an error message will be returned with the appropriate HTTP status code. Both timed out and internal server errors will only have the appropriate status codes and not this body. It's important to expect some extra time with the analysis endpoint as it takes time to get the results.
```
{
    "msg": string
}
```

## Evaluating results
In order to perform evaluation of the generated chords compared to manually plotted chords, first an updated songs.json must be placed in the ```/Data/``` folder. Then, add the following lines to main.py:
```
import evaluation

evaluator = evaluation.Evaluators()
evaluator.batchHandler()
```
The batchHandler method takes four parameters. The first allows for forced reevaluation of previously evaluated and stored chords. The second gives the option to take the aggregated results and generate, save to CSV files and plot these aggregates. The third controls whether the handler should print IDs and results to screen. These options all default to 'False'. The fourth and final allows you to pass in a neural network model - the default is 'None', in which case it then uses the algorithm solution instead of a neural network solution.

- Parameters:
```
{
    "force": bool,
    "plot": bool,
    "verbose": bool,
    "model": keras.models.Sequential
}
```

The output from this evaluation will be added to ```/Data/evaluatedSongs.json```. At first it is stored as individual files in ```/Data/Results/Songs/``` because the process will likely take many hours and this allows processed results to be saved in case of interruption. When run, batchHandler automatically checks this path for new songs, appends them to ```/Data/evaluatedSongs.json``` , and then deletes the directory and its files. Additionally, CSV-files with more grouping data will be generated in ```/Data/Results/``` folder if the "plot" option is selected. This folder also holds ```detailedResults.json```