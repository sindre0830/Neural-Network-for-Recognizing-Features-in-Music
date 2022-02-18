package results

import (
	debug "main/Debug"
	"net/http"
)

func MethodHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		getResults(w)
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
