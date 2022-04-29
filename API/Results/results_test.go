package results

import "testing"

func TestCheckChord(t *testing.T) {
	testData := map[string]bool{
		"A":   true,
		"E#":  false,
		"":    false,
		"hei": false,
	}

	for test, expected := range testData {
		res := checkChord(test)
		if res != expected {
			t.Errorf("Tested: %v. Expected: %v. Got: %v.", test, expected, res)
		}
	}
}
