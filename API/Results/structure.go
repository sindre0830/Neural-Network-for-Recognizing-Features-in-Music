package results

// Update stores the new values of a song
type Update struct {
	Approved bool      `json:"approved"`
	Title    string    `json:"title"`
	Bpm      float64   `json:"bpm"`
	Beats    []float64 `json:"beats"`
	Chords   []string  `json:"chords"`
}
