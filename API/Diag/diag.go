package diag

import (
	"encoding/json"
	datahandling "main/DataHandling"
	database "main/Database"
	debug "main/Debug"
	dictionary "main/Dictionary"
	"net/http"
)

// get handles get requests to the diag endpoint
func (diag *Diag) get(w http.ResponseWriter, r *http.Request) {
	w.Header().Add("Content-Type", "application/json")
	var errorMsg debug.Debug

	// get model status
	status, err := getModelStatus()
	if err != nil {
		errorMsg.Update(
			status,
			"diag.get() -> Getting status of model",
			err.Error(),
			"Unknown",
		)
		errorMsg.Print()
	}

	diag.ModelConnection = status

	// get processing songs
	diag.ProcessingSongs, err = getSongs("processing")
	if err != nil {
		errorMsg.Update(
			http.StatusInternalServerError,
			"diag.get() -> Getting processing songs",
			err.Error(),
			"Unknown",
		)
		errorMsg.Print()
	}

	// get failed songs
	diag.FailedSongs, err = getSongs("failed")
	if err != nil {
		errorMsg.Update(
			http.StatusInternalServerError,
			"diag.get() -> Getting failed songs",
			err.Error(),
			"Unknown",
		)
		errorMsg.Print()
	}

	// encode data
	json.NewEncoder(w).Encode(diag)
}

// getModelStatus gets the status of the model.
func getModelStatus() (int, error) {
	_, status, err := datahandling.Request(dictionary.NN_URL + dictionary.NN_DIAG)
	if err != nil {
		return status, err
	}

	return http.StatusOK, nil
}

// getSongs get all songs based on a query from the database.
func getSongs(query string) ([]string, error) {
	data := make([]map[string]interface{}, 0)
	// get all processing songs from the database
	data, err := database.Firestore.GetAll(dictionary.RESULTS_COLLECTION, query)
	if err != nil {
		return nil, err
	}

	// retrieve the titles of all documents
	var title []string
	for _, el := range data {
		title = append(title, el["title"].(string))
	}

	return title, nil
}
