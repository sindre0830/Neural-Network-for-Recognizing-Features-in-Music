package dictionary

import "os"

/* info */
const VERSION = "v1"

/* endpoint paths */
const ANALYSIS_PATH = "/" + VERSION + "/analysis"
const RESULTS_PATH = "/" + VERSION + "/results"
const DIAG_PATH = "/" + VERSION + "/diag"

/* database collections */
const RESULTS_COLLECTION = "results"

/* urls */
const YOUTUBE_URL = "https://www.googleapis.com/youtube/v3/videos?part=snippet&fields=items"

/* api keys */
var YOUTUBE_KEY string

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
