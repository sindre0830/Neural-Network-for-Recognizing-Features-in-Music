package results

import (
	"encoding/json"
	database "main/Database"
	debug "main/Debug"
	"net/http"
)

// getResults gets all song results from the database
func getResults(w http.ResponseWriter) {
	w.Header().Add("Content-Type", "application/json")

	data := make([]map[string]interface{}, 0)
	data, err := database.Firestore.GetAll("songs")
	if err != nil {
		var errorMsg debug.Debug
		errorMsg.Update(
			http.StatusInternalServerError,
			"getResults() -> Getting results from database",
			err.Error(),
			"Unknown",
		)
		return
	}

	// encode data
	json.NewEncoder(w).Encode(data)
}
