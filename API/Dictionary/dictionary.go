package dictionary

/* info */
const VERSION = "v1"

/* endpoint paths */
const ANALYSIS_PATH = "/" + VERSION + "/analysis"
const RESULTS_PATH = "/" + VERSION + "/results"
const DIAG_PATH = "/" + VERSION + "/diag"

/* database collections */
const RESULTS_COLLECTION = "results"

/* urls */
const YOUTUBE_URL = "https://www.youtube.com/oembed"
const NN_URL = "http://localhost:5000/v1/"

/* nn endpoints */
const NN_ANALYSIS = "analysis"
const NN_REMOVE = "remove"
const NN_DIAG = "diag"

/* other values */
var CHORDS = []string{"C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "Cm", "C#m", "Dm", "D#m", "Em", "Fm", "F#m", "Gm", "G#m", "Am", "A#m", "Bm"}
