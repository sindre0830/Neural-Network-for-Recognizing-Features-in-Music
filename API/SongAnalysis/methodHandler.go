package songanalysis

import (
	debug "main/Debug"
	"net/http"
)

// MethodHandler handles the http request based on method
func MethodHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodPost:
	default:
		var errorMsg debug.Debug
		errorMsg.Update(
			http.StatusMethodNotAllowed,
			"MethodHandler() -> Method validating",
			"method validation: validating method",
			"Method not implemented",
		)
	}
}