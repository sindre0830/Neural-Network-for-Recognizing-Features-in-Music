package results

import (
	"encoding/json"
	"errors"
	datahandling "main/DataHandling"
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
		http.Error(w, errorMsg.PossibleReason, errorMsg.StatusCode)
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
			"Invalid body",
		)
		errorMsg.Print()
		http.Error(w, errorMsg.PossibleReason, errorMsg.StatusCode)
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
		http.Error(w, errorMsg.PossibleReason, errorMsg.StatusCode)
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

	// clean up cached data on the NN side
	status, err := cleanUp(id[0])
	if err != nil {
		errorMsg.Update(
			status,
			"update() -> cleanUp() -> Clean up audio files",
			err.Error(),
			"Unknown",
		)
		errorMsg.Print()
	}

	http.Error(w, "Document successfully updated", http.StatusOK)
}

// addToMap moves the data from a structure to a map.
func addToMap(update Update) map[string]interface{} {
	// add the values that are not null to the data map
	data := make(map[string]interface{})
	if update.Title != "" {
		data["title"] = update.Title
	}
	if update.Bpm != 0 {
		data["bpm"] = update.Bpm
	}
	if update.Beats != nil {
		data["beats"] = update.Beats
	}
	if update.Chords != nil {
		// make sure the slice only contains valid chords
		for _, v := range update.Chords {
			if !checkChord(v) {
				return nil
			}
		}
		data["chords"] = update.Chords
	}
	// add approved label
	data["approved"] = update.Approved
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

// cleanUp removes requests that the NN API removes the song's audio files.
func cleanUp(id string) (int, error) {
	body, status, err := datahandling.Request(dictionary.NN_URL + dictionary.NN_REMOVE + "?id=" + id)
	if err != nil {
		return status, err
	}

	// only get error message if there is a body
	// everything went fine if there is not
	if len(body) > 0 {
		var data map[string]string
		err = json.Unmarshal(body, &data)
		if err != nil {
			return http.StatusInternalServerError, err
		}
		return http.StatusBadRequest, errors.New(data["msg"])
	}

	return status, nil
}
