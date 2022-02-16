package results

// Song stores information about a song
type Song struct {
	title       string
	beats       []float64
	parts       []map[string]interface{}
	arrangement []map[string]interface{}
	startTime   float64
}

// Result stores the result of the song analysis
type Result struct {
	title string
	beats []float64
	parts []struct {
		length int
		chords []struct {
			chord  int
			minor  bool
			length int
		}
	}
	arrangement []struct {
		part        int
		repetitions int
	}

	startTime float64
}
