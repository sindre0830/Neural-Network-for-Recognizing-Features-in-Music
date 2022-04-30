package diag

import (
	debug "main/Debug"
	"net/http"
)

// MethodHandler handles the http request based on method.
func MethodHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		var diag Diag
		diag.get(w, r)
	default:
		var errorMsg debug.Debug
		errorMsg.Update(
			http.StatusMethodNotAllowed,
			"StatusHandler() -> Method validating",
			"method validation: validating method",
			"Method not implemented",
		)
		http.Error(w, http.StatusText(errorMsg.StatusCode), errorMsg.StatusCode)
	}
}
