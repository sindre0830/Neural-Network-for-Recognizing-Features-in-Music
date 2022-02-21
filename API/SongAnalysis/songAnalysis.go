package songanalysis

import (
	"encoding/json"
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
}
