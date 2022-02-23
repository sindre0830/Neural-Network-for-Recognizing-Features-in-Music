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
	var errorMsg debug.Debug

	// validate URL
	path := strings.Split(r.URL.Path, "/")
	if len(path) != 3 {
		errorMsg.Update(
			http.StatusBadRequest,
			"update() -> Validating URL",
			"url validation: incorrect format",
			"URL format not valid",
		)
		errorMsg.Print()
		return
	}

	// make sure an ID is provided by the user
	id := path[2]
	if len(id) < 1 {
		errorMsg.Update(
			http.StatusBadRequest,
			"update() -> Validating URL",
			"url validation: incorrect format",
			"URL format not valid",
		)
		errorMsg.Print()
		return
	}

	// decode body to a map
	var data map[string]interface{}
	err := json.NewDecoder(r.Body).Decode(&data)
	if err != nil {
		errorMsg.Update(
			http.StatusBadRequest,
			"update() -> Decoding body",
			err.Error(),
			"Unknown",
		)
		errorMsg.Print()
		return
	}

	// update data in database
	err = database.Firestore.Update("songs", id, data)
	if err != nil {
		errorMsg.Update(
			http.StatusInternalServerError,
			"update() -> Updating data in database",
			err.Error(),
			"Unknown",
		)
		errorMsg.Print()
		return
	}

	http.Error(w, "Document successfully updated", http.StatusOK)
}
