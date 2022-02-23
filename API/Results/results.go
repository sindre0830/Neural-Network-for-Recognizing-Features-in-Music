package results

import (
	"encoding/json"
	database "main/Database"
	debug "main/Debug"
	"net/http"
	"strings"
)

// get gets all song results from the database.
func get(w http.ResponseWriter, r *http.Request) {
	w.Header().Add("Content-Type", "application/json")

	data := make([]map[string]interface{}, 0)
	// get all documents from the database
	data, err := database.Firestore.GetAll("songs")
	if err != nil {
		var errorMsg debug.Debug
		errorMsg.Update(
			http.StatusInternalServerError,
			"getResults() -> Getting results from database",
			err.Error(),
			"Unknown",
		)
		errorMsg.Print()
		return
	}

	// encode data
	json.NewEncoder(w).Encode(data)
}

// update updates a song in the database.
func update(w http.ResponseWriter, r *http.Request) {
	// validate URL
	path := strings.Split(r.URL.Path, "/")
	if len(path) != 3 {
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

	// make sure an ID is provided by the user
	id := path[2]
	if len(id) < 1 {
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
}
