package songanalysis

import (
	"encoding/json"
	"fmt"
	debug "main/Debug"
	"net/http"
	"strings"
)

// post sends a YouTube link
func post(w http.ResponseWriter, r *http.Request) {
	// validate URL
	path := strings.Split(r.URL.Path, "/")
	if len(path) != 2 {
		var errorMsg debug.Debug
		errorMsg.Update(
			http.StatusBadRequest,
			"post() -> Validating URL",
			"url validation: incorrect format",
			"URL format not valid",
		)
		errorMsg.Print()
		return
	}

	// decode body to song structure
	var song Song
	err := json.NewDecoder(r.Body).Decode(&song)
	if err != nil {
		var errorMsg debug.Debug
		errorMsg.Update(
			http.StatusBadRequest,
			"post() -> Decoding body",
			err.Error(),
			"JSON format not valid",
		)
		errorMsg.Print()
		return
	}

	// check if a link is sent
	if len(song.Link) <= 0 {
		var errorMsg debug.Debug
		errorMsg.Update(
			http.StatusBadRequest,
			"post() -> Parsing body",
			"json: not a valid json format",
			"JSON format not valid",
		)
		errorMsg.Print()
		return
	}

	// get the id from the link
	linkArr := strings.Split(song.Link, "=")
	var id string
	// there are two ways to send a link, so we will have to check which link format is sent to be able to retrieve the id
	if len(linkArr) <= 1 {
		id = strings.Split(song.Link, "/")[3]
	} else {
		id = linkArr[1]
	}

	fmt.Println(id)
}
