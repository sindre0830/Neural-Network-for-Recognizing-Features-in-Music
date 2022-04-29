package results

import (
	"encoding/json"
	database "main/Database"
	debug "main/Debug"
	dictionary "main/Dictionary"
	"net/http"
)

// get all song results from the database.
func get(w http.ResponseWriter, r *http.Request) {
	w.Header().Add("Content-Type", "application/json")

	data := make([]map[string]interface{}, 0)
	// get all documents from the database
	data, err := database.Firestore.GetAll(dictionary.RESULTS_COLLECTION, "")
	if err != nil {
		var errorMsg debug.Debug
		errorMsg.Update(
			http.StatusInternalServerError,
			"getResults() -> database.GetAll() -> Getting results from database",
			err.Error(),
			"Unknown",
		)
		errorMsg.Print()
		http.Error(w, http.StatusText(errorMsg.StatusCode), errorMsg.StatusCode)
		return
	}

	// encode data
	json.NewEncoder(w).Encode(data)
}

// update a song in the database.
func update(w http.ResponseWriter, r *http.Request) {
	var errorMsg debug.Debug

	// validate URL by extracting the id
	id, ok := r.URL.Query()["id"]
	if !ok || len(id[0]) < 1 {
		errorMsg.Update(
			http.StatusBadRequest,
			"update() -> Validating URL",
			"url validation: incorrect format",
			"Missing 'id' param",
		)
		errorMsg.Print()
		http.Error(w, http.StatusText(errorMsg.StatusCode), errorMsg.StatusCode)
		return
	}

	// decode body to a map
	var update Update
	err := json.NewDecoder(r.Body).Decode(&update)
	if err != nil {
		errorMsg.Update(
			http.StatusBadRequest,
			"update() -> Decoding body",
			err.Error(),
			"Unknown",
		)
		errorMsg.Print()
		http.Error(w, http.StatusText(errorMsg.StatusCode), errorMsg.StatusCode)
		return
	}

	// add to map to be able to merge with the firebase document
	data := addToMap(update)
	if data == nil {
		errorMsg.Update(
			http.StatusBadRequest,
			"update() -> Validating user input",
			"input validation: invalid values",
			"Invalid Chords values",
		)
		errorMsg.Print()
		http.Error(w, http.StatusText(errorMsg.StatusCode), errorMsg.StatusCode)
		return
	}

	// update data in database
	err = database.Firestore.Update(dictionary.RESULTS_COLLECTION, id[0], data)
	if err != nil {
		errorMsg.Update(
			http.StatusInternalServerError,
			"update() -> database.Update() -> Updating data in database",
			err.Error(),
			"Unknown",
		)
		errorMsg.Print()
		http.Error(w, http.StatusText(errorMsg.StatusCode), errorMsg.StatusCode)
		return
	}

	http.Error(w, "Document successfully updated", http.StatusOK)
}

// addToMap moves the data from a structure to a map.
func addToMap(update Update) map[string]interface{} {
	// add the values that are not null to the data map
	data := make(map[string]interface{})
	if update.Title != "" {
		data["Title"] = update.Title
	}
	if update.Bpm != 0 {
		data["Bpm"] = update.Bpm
	}
	if update.Beats != nil {
		data["Beats"] = update.Beats
	}
	if update.Chords != nil {
		// make sure the slice only contains valid chords
		for _, v := range update.Chords {
			if !checkChord(v) {
				return nil
			}
		}
		data["Chords"] = update.Chords
	}
	return data
}

// checkChord checks if the given value is a valid chord.
func checkChord(value string) bool {
	for _, el := range dictionary.CHORDS {
		if el == value {
			return true
		}
	}
	return false
}
