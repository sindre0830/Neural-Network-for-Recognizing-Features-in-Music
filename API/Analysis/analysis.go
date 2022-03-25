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
func sendToAnalysis(w http.ResponseWriter, r *http.Request) {
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

	// get result of analysis
	var analysis Analysis
	err, status := analysis.getAnalysis(id)
	if err != nil {
		var errorMsg debug.Debug
		errorMsg.Update(
			status,
			"analysis.post() -> Getting result of analysis",
			err.Error(),
			"Unknown",
		)
		errorMsg.Print()
		http.Error(w, errorMsg.RawError, errorMsg.StatusCode)
		return
	}

	// add result to database
	err, status = analysis.addToDatabase(id)
	if err != nil {
		var errorMsg debug.Debug
		errorMsg.Update(
			status,
			"analysis.post() -> Adding result to database",
			err.Error(),
			"Unknown",
		)
		errorMsg.Print()
		http.Error(w, errorMsg.RawError, errorMsg.StatusCode)
	}

	http.Error(w, "song successfully analyzed", http.StatusOK)
}

// getAnalysis analysis result.
func (analysis *Analysis) getAnalysis(id string) (error, int) {
	// create request
	body, status, err := dataHandling.Request("http://localhost:8081/get?id=" + id)
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

// addToDatabase adds the analysis result to the database.
func (analysis *Analysis) addToDatabase(id string) (error, int) {
	// get title of youtube video
	body, status, err := dataHandling.Request(dictionary.GetYouTubeURL(id))
	if err != nil {
		return err, status
	}

	// unmarshal to map
	var items map[string][]interface{}
	err = json.Unmarshal(body, &items)
	if err != nil {
		return err, http.StatusInternalServerError
	}

	// add information to database structure
	var resultDB dictionary.ResultDB
	resultDB.Bpm = analysis.Bpm
	resultDB.Beats = analysis.Beats
	resultDB.Chords = analysis.Chords
	resultDB.Title = items["items"][0].(map[string]interface{})["snippet"].(map[string]interface{})["title"].(string)
	resultDB.Approved = false

	err = database.Firestore.Add(dictionary.RESULTS_COLLECTION, id, resultDB)
	if err != nil {
		return err, http.StatusInternalServerError
	}

	return nil, http.StatusOK
}
