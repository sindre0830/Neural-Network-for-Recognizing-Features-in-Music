package results

// Result stores the result of the song analysis
type Result struct {
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
