package songanalysis

import (
	"net/http"
	"strings"
)

// post sends a YouTube link
func post(w http.ResponseWriter, r *http.Request) {
	// validate URL
	path := strings.Split(r.URL.Path, "/")
	if len(path) != 2 {
		var errorMsg debug.Debug
		debug.Update(
			http.StatusBadRequest,
			"post() -> Validating URL",
			"url validation: incorrect format",
			"URL format not valid",
		)
	}
}
