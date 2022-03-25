package dataHandling

import (
	"io/ioutil"
	"net/http"
)

// Request gets data from an URL.
func Request(url string) ([]byte, int, error) {
	// create request
	req, err := http.NewRequest(http.MethodGet, url, nil)
	if err != nil {
		return nil, req.Response.StatusCode, err
	}

	client := &http.Client{}

	// do request
	res, err := client.Do(req)
	if err != nil {
		return nil, res.StatusCode, err
	}

	// read body of request
	body, err := ioutil.ReadAll(res.Body)
	if err != nil {
		return nil, http.StatusInternalServerError, err
	}

	return body, http.StatusOK, err
}
