package analysis

import (
	"encoding/json"
	"fmt"
	dataHandling "main/DataHandling"
	debug "main/Debug"
	dictionary "main/Dictionary"
	"net/http"
	"strings"
)

// sendToAnalysis handles retrieving and sending of a YouTube link.
func analyze(w http.ResponseWriter, r *http.Request) {
	// decode body to song structure
	var song Song
	err := json.NewDecoder(r.Body).Decode(&song)
	if err != nil {
		var errorMsg debug.Debug
		errorMsg.Update(
			http.StatusBadRequest,
			"analysis.post() -> Decoding body",
			err.Error(),
			"JSON format not valid",
		)
		errorMsg.Print()
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// check if a link is sent
	if song.Link == "" {
		var errorMsg debug.Debug
		errorMsg.Update(
			http.StatusBadRequest,
			"analysis.post() -> Parsing body",
			"json: not a valid json format",
			"JSON format not valid",
		)
		errorMsg.Print()
		http.Error(w, errorMsg.RawError, http.StatusBadRequest)
		return
	}

	// retrieve the id from the link
	linkArr := strings.Split(song.Link, "=")
	var id string

	// there are two ways to send a youtube link, so we have to check which link format is sent to be able to retrieve the id
	if len(linkArr) <= 1 {
		id = strings.Split(song.Link, "/")[3]
	} else {
		id = linkArr[1]
	}

	fmt.Println(id)

	// get title of video
	title, err, status := getTitle(id)
	if err != nil {
		var errorMsg debug.Debug
		errorMsg.Update(
			status,
			"analysis.post() -> Getting title of YouTube video",
			err.Error(),
			"Unknown",
		)
		errorMsg.Print()
		http.Error(w, errorMsg.RawError, errorMsg.StatusCode)
		return
	}

	fmt.Println(title)

	http.Error(w, "song successfully analyzed", http.StatusOK)
}

// getTitle gets the title of a YouTube video based on the id.
func getTitle(id string) (string, error, int) {
	// get title of youtube video
	body, status, err := dataHandling.Request(dictionary.GetYouTubeURL(id))
	if err != nil {
		return "", err, status
	}

	// unmarshal to map
	var items map[string][]interface{}
	err = json.Unmarshal(body, &items)
	if err != nil {
		return "", err, http.StatusInternalServerError
	}

	title := items["items"][0].(map[string]interface{})["snippet"].(map[string]interface{})["title"].(string)

	return title, nil, http.StatusOK
}
