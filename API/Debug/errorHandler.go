package debug

import (
	"fmt"
	"net/http"
	"time"
)

// Debug structure stores information about errors.
//
// Functionality: Update, Print
type Debug struct {
	StatusCode     int    `json:"status_code"`
	Location       string `json:"location"`
	RawError       string `json:"raw_error"`
	PossibleReason string `json:"possible_reason"`
}

// Update sets new data in structure.
func (debug *Debug) Update(status int, loc string, err string, reason string) {
	debug.StatusCode = status
	debug.Location = loc
	debug.RawError = err
	// update reason if status code shows client error
	if status == http.StatusBadRequest || status == http.StatusNotFound || status == http.StatusMethodNotAllowed {
		debug.PossibleReason = reason
	} else {
		debug.PossibleReason = "Unknown"
	}
}

// Print sends structure to console.
func (debug *Debug) Print() {
	// send output to console
	fmt.Printf(
		"%v {\n"+
			"    status_code:     %v,\n"+
			"    location:        %s,\n"+
			"    raw_error:       %s,\n"+
			"    possible_reason: %s \n"+
			"}\n",
		time.Now().Format("2006-01-02 15:04:05"), debug.StatusCode, debug.Location, debug.RawError, debug.PossibleReason,
	)
}
