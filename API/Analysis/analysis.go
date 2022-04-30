package analysis

import (
	"encoding/json"
	"log"
	datahandling "main/DataHandling"
	database "main/Database"
	debug "main/Debug"
	dictionary "main/Dictionary"
	"net/http"
	"net/url"
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
		http.Error(w, http.StatusText(errorMsg.StatusCode), errorMsg.StatusCode)
		return
	}

	// get id of song, if the link is valid
	id := getID(song.Link)
	if id == song.Link {
		errorMsg.Update(
			http.StatusBadRequest,
			"analysis.post() -> Parsing body",
			"",
			"Body not valid",
		)
		errorMsg.Print()
		http.Error(w, http.StatusText(errorMsg.StatusCode), errorMsg.StatusCode)
		return
	}

	// get title of video
	title, status, err := getTitle(id)
	if err != nil {
		errorMsg.Update(
			status,
			"analysis.post() -> Getting title of YouTube video",
			err.Error(),
			"Unknown",
		)
		errorMsg.Print()
		http.Error(w, http.StatusText(errorMsg.StatusCode), errorMsg.StatusCode)
		return
	}

	// add title to database, marked as processing
	data := map[string]interface{}{
		"title":      title,
		"processing": true,
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
		http.Error(w, http.StatusText(errorMsg.StatusCode), errorMsg.StatusCode)
		return
	}

	// used for updating the result in the database
	result := make(map[string]interface{})

	// get result of analysis
	var analysis Analysis
	status, err = analysis.getAnalysis(id)
	if err != nil {
		// mark song as failed
		result["failed"] = true
		result["processing"] = false

		errorMsg.Update(
			status,
			"analysis.post() -> Getting result of analysis",
			err.Error(),
			"Unknown",
		)
		errorMsg.Print()
	} else {
		// initialize result map with result
		result["failed"] = false
		result["processing"] = false
		result["approved"] = false
		result["bpm"] = analysis.Bpm
		result["beats"] = analysis.Beats
		result["chords"] = analysis.Chords
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
		http.Error(w, http.StatusText(errorMsg.StatusCode), errorMsg.StatusCode)
		return
	}

	// return status based on if the song failed or not
	if result["failed"].(bool) {
		http.Error(w, "Song failed", status)
	} else {
		http.Error(w, "Song successfully analyzed", http.StatusOK)
	}
}

// getID retrieves the ID of a YouTube video from the link.
func getID(link string) string {
	// remove whitespace from link
	trimmedLink := strings.ReplaceAll(link, " ", "")

	// parse the link to an url
	u, err := url.Parse(trimmedLink)
	if err != nil {
		return link
	}

	// youtube links have two different formats, so there needs to be two different ways of retrieving them
	if strings.HasPrefix(trimmedLink, "https://youtu.be/") {
		return u.Path[1:]
	} else if strings.HasPrefix(trimmedLink, "https://www.youtube.com/") {
		id, err := url.ParseQuery(u.RawQuery)
		if err != nil {
			log.Fatal(err)
		}
		return id["v"][0]
	} else {
		// if it is not a valid link, return the same value as inputted
		return link
	}
}

// getTitle gets the title of a YouTube video based on the id.
func getTitle(id string) (string, int, error) {
	u, err := url.Parse(dictionary.YOUTUBE_URL)
	if err != nil {
		return "", http.StatusInternalServerError, err
	}

	// construct url
	q := u.Query()
	q.Set("format", "json")
	q.Set("url", "https://www.youtube.com/watch?v="+id)
	u.RawQuery = q.Encode()

	// send request
	body, status, err := datahandling.Request(u.String())
	if err != nil {
		return "", status, err
	}

	// unmarshal to map
	var data map[string]interface{}
	err = json.Unmarshal(body, &data)
	if err != nil {
		return "", http.StatusInternalServerError, err
	}

	return data["title"].(string), http.StatusOK, nil
}

// getAnalysis result.
func (analysis *Analysis) getAnalysis(id string) (int, error) {
	// create request
	body, status, err := datahandling.Request(dictionary.NN_URL + dictionary.NN_ANALYSIS + "?id=" + id)
	if err != nil {
		return status, err
	}

	// unmarshal to struct
	err = json.Unmarshal(body, &analysis)
	if err != nil {
		return http.StatusInternalServerError, err
	}

	return http.StatusOK, nil
}
