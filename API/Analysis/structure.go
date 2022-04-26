package analysis

// Song stores a YouTube link
type Song struct {
	Link string `json:"link"`
}

// Analysis stores the result from the analysis
type Analysis struct {
	Bpm    float64   `json:"bpm"`
	Beats  []float64 `json:"beats"`
	Chords []string  `json:"chords"`
}
