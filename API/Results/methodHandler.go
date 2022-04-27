package results

import (
	debug "main/Debug"
	"net/http"
)

// MethodHandler handles the http request based on method
func MethodHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		get(w, r)
	case http.MethodPut:
		update(w, r)
	default:
		var errorMsg debug.Debug
		errorMsg.Update(
			http.StatusMethodNotAllowed,
			"MethodHandler() -> Method validating",
			"method validation: validating method",
			"Method not implemented",
		)
		errorMsg.Print()
		http.Error(w, http.StatusText(errorMsg.StatusCode), errorMsg.StatusCode)
	}
}
