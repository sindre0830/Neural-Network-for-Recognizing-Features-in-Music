package results

import "testing"

func TestAddToMap(t *testing.T) {
	testData := []struct {
		update   Update
		expected map[string]interface{}
	}{
		{
			update: Update{
				Title:  "New title",
				Bpm:    213.42,
				Beats:  []float64{2.34, 5.34, 8.24},
				Chords: []string{"A", "C#", "A"},
			},
			expected: map[string]interface{}{
				"Title":    "New title",
				"Bpm":      213.42,
				"Beats":    []float64{2.34, 5.34, 8.24},
				"Chords":   []string{"A", "C#", "A"},
				"Approved": true,
			},
		},
		{
			update: Update{
				Bpm:    23,
				Chords: []string{"C", "A"},
			},
			expected: map[string]interface{}{
				"Bpm":      23,
				"Chords":   []string{"C", "A"},
				"Approved": true,
			},
		},
		{
			update: Update{
				Chords: []string{"E#", "A"},
			},
			expected: nil,
		},
	}

	for _, test := range testData {
		res := addToMap(test.update)
		if len(res) != len(test.expected) {
			t.Errorf("Tested: %v. Expected: %v. Got: %v.", test.update, test.expected, res)
		}
	}
}

func TestCheckChord(t *testing.T) {
	testData := map[string]bool{
		"A":   true,
		"":    true,
		"E#":  false,
		"hei": false,
	}

	for test, expected := range testData {
		res := checkChord(test)
		if res != expected {
			t.Errorf("Tested: %v. Expected: %v. Got: %v.", test, expected, res)
		}
	}
}
