package dictionary

import "os"

/* info */
var VERSION = "v1"

/* endpoint paths */
var ANALYSIS_PATH = "/" + VERSION + "/analysis"
var RESULTS_PATH = "/" + VERSION + "/results"
var DIAG_PATH = "/" + VERSION + "/diag"

/* firebase collections */
var RESULTS_COLLECTION = "results"

/* urls */
var YOUTUBE_URL = "https://www.googleapis.com/youtube/v3/videos?part=snippet&fields=items"

/* api keys */
var YOUTUBE_KEY string

/* global structure */
// ResultDB is the structure used for the results in the database
type ResultDB struct {
	Title    string
	Approved bool
	Bpm      float64
	Beats    []float64
	Chords   []string
}

/* functions */
// GetYouTubeKey reads the API key of the YouTube API from a file.
func GetYouTubeKey() (string, error) {
	data, err := os.ReadFile("./apiKey.txt")
	if err != nil {
		return "", err
	}

	return string(data), err
}

// GetYouTubeURL creates the complete URL for the YouTube API.
func GetYouTubeURL(id string) string {
	return YOUTUBE_URL + "&id=" + id + "&key=" + YOUTUBE_KEY
}
