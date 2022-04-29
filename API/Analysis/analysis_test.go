package analysis

import (
	"testing"
)

func TestGetID(t *testing.T) {
	testData := map[string]string{
		"https://www.youtube.com/watch?v=wpEmiXZEKo8":     "wpEmiXZEKo8",
		"https://youtu.be/ngzC_8zqInk":                    "ngzC_8zqInk",
		"www.youtube.com":                                 "www.youtube.com",
		"https://www.youtube.com/watch?v= wpEm  iX ZEKo8": "wpEmiXZEKo8",
		"hello world": "hello world",
		"":            "",
	}

	for test, expected := range testData {
		res := getID(test)
		if res != expected {
			t.Errorf("Tested: %v. Expected: %v. Got: %v.", test, expected, res)
		}
	}
}
