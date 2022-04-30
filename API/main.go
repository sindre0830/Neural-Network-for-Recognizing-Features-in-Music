package main

import (
	"log"
	analysis "main/Analysis"
	database "main/Database"
	diag "main/Diag"
	dictionary "main/Dictionary"
	results "main/Results"
	"net/http"
	"os"
)

// main program.
func main() {
	// get port
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	// set up firebase
	err := database.Firestore.Setup()
	if err != nil {
		defer database.Firestore.Client.Close()
		log.Fatalln(err)
	}

	// path to all endpoints
	http.HandleFunc(dictionary.ANALYSIS_PATH, analysis.MethodHandler)
	http.HandleFunc(dictionary.RESULTS_PATH, results.MethodHandler)
	http.HandleFunc(dictionary.DIAG_PATH, diag.MethodHandler)

	log.Fatal(http.ListenAndServe(":"+port, nil))
}
