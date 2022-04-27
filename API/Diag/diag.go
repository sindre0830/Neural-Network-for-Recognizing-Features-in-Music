package diag

import (
	"encoding/json"
	dataHandling "main/DataHandling"
	database "main/Database"
	debug "main/Debug"
	dictionary "main/Dictionary"
	"net/http"
)

// get handles get requests to the diag endpoint
func (diag *Diag) get(w http.ResponseWriter, r *http.Request) {
	var errorMsg debug.Debug

	// get model status
	err, status := getModelStatus()
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
	diag.ProcessingSongs, err = getSongs("Processing")
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
	diag.FailedSongs, err = getSongs("Failed")
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
func getModelStatus() (error, int) {
	_, status, err := dataHandling.Request("http://localhost:8082/status")
	if err != nil {
		return err, status
	}

	return nil, http.StatusOK
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
		title = append(title, el["Title"].(string))
	}

	return title, nil
}