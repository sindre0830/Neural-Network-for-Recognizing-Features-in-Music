package analysis

import (
	"encoding/json"
	dataHandling "main/DataHandling"
	database "main/Database"
	debug "main/Debug"
	dictionary "main/Dictionary"
	"net/http"
	"strings"
)

// sendToAnalysis handles retrieving and sending of a YouTube link.
func analyze(w http.ResponseWriter, r *http.Request) {
	var errorMsg debug.Debug

	// decode body to song structure
	var song Song
	err := json.NewDecoder(r.Body).Decode(&song)
	if err != nil {
		errorMsg.Update(
			http.StatusBadRequest,
			"analysis.post() -> Decoding body",
			err.Error(),
			"JSON format not valid",
		)
		errorMsg.Print()
		return
	}

	// check if a link is sent
	if song.Link == "" {
		errorMsg.Update(
			http.StatusBadRequest,
			"analysis.post() -> Parsing body",
			"json: not a valid json format",
			"JSON format not valid",
		)
		errorMsg.Print()
		return
	}

	// get id of song
	id := getID(song.Link)

	// get title of video
	title, err, status := getTitle(id)
	if err != nil {
		errorMsg.Update(
			status,
			"analysis.post() -> Getting title of YouTube video",
			err.Error(),
			"Unknown",
		)
		errorMsg.Print()
		return
	}

	// add title to database, marked as processing
	data := map[string]interface{}{
		"Title":      title,
		"Processing": true,
	}
	err = database.Firestore.Add(dictionary.RESULTS_COLLECTION, id, data)
	if err != nil {
		errorMsg.Update(
			http.StatusInternalServerError,
			"analysis.post() -> Adding song to database",
			err.Error(),
			"Unknown",
		)
		errorMsg.Print()
		return
	}

	// used for updating the result in the database
	result := make(map[string]interface{})

	// get result of analysis
	var analysis Analysis
	err, status = analysis.getAnalysis(id)
	if err != nil {
		// mark song as failed
		result["Failed"] = true
		result["Processing"] = false

		errorMsg.Update(
			status,
			"analysis.post() -> Getting result of analysis",
			err.Error(),
			"Unknown",
		)
		errorMsg.Print()
	} else {
		// initialize result map with result
		result["Failed"] = false
		result["Processing"] = false
		result["Approved"] = false
		result["Bpm"] = analysis.Bpm
		result["Beats"] = analysis.Beats
		result["Chords"] = analysis.Chords
	}

	// update database with the result
	err = database.Firestore.Update(dictionary.RESULTS_COLLECTION, id, result)
	if err != nil {
		errorMsg.Update(
			status,
			"analysis.post() -> Updating result in database",
			err.Error(),
			"Unknown",
		)
		errorMsg.Print()
		return
	}

	// return status based on if the song failed or not
	if result["Failed"].(bool) {
		http.Error(w, "Song failed", status)
	} else {
		http.Error(w, "Song successfully analyzed", http.StatusOK)
	}
}

// getID retrieves the ID of a YouTube video from the link.
func getID(link string) string {
	// retrieve the id from the link
	linkArr := strings.Split(link, "=")
	var id string

	// there are two ways to send a youtube link, so we have to check which link format is sent to be able to retrieve the id
	if len(linkArr) <= 1 {
		id = strings.Split(link, "/")[3]
	} else {
		id = linkArr[1]
	}

	return id
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

// getAnalysis result.
func (analysis *Analysis) getAnalysis(id string) (error, int) {
	// create request
	body, status, err := dataHandling.Request("http://localhost:8082/analysis?id=" + id)
	if err != nil {
		return err, status
	}

	// unmarshal to struct
	err = json.Unmarshal(body, &analysis)
	if err != nil {
		return err, http.StatusInternalServerError
	}

	return nil, http.StatusOK
}
