package diag

import (
	debug "main/Debug"
	"net/http"
)

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
	}
}
