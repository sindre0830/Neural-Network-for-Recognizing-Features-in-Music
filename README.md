# Neural-Network-for-Recognizing-Features-in-Music
Bachelor Thesis - Spring 2022

## Info
- Authors:
    - Sindre Eiklid (sindreik@stud.ntnu.no)
    - Rickard Loland (rickarl@stud.ntnu.no)
    - Maren Skårestuen Grindal (marensg@stud.ntnu.no)
- Final report: [link here]()
- Website address: [localhost:3000/](localhost:3000/)

## Instructions
0. Download [Docker](https://docs.docker.com/get-docker/)
1. Run the command ```docker compose up``` to build the images and run the containers.
    - To stop the containers run the command ```docker compose stop```
    - To start the containers run the command ```docker compose start```

Note: The application is programmed to start when the server starts. To stop this, edit the ```docker-compose.yml``` file by removing the ```restart: always``` lines. You will have to build the containers again by running ```docker compose down``` then start at instructions again.

## Usage
Open the website at [localhost:3000/](localhost:3000/) and utilize the functionality through the UI.

#### Main page
[localhost:3000/](localhost:3000/) brings you to the main page, here you can input a youtube link to analyze. When you submit a song it will say ```Parsing link...```, once it is finished it will say ```Song successfully analyzed, the result is uploaded to the results page```.

#### Results page
[http://localhost:3000/results](http://localhost:3000/results) brings you to the result page, here you can see all the results from song analysis. It allows you to edit the result if you wish and approve the song. Once it is approved, the results are locked in. If you wish to edit it again, you can unapprove the songs. If you want to remove any results from the databse, you can click the trashcan icon.

#### Status page
[http://localhost:3000/status](http://localhost:3000/status) brings you to the status page, here you can see the current songs that are being analyzed, failed songs, and the status of each endpoint.
