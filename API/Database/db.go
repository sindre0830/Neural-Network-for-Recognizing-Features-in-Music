package database

import (
	"context"
	debug "main/Debug"
	"net/http"

	"cloud.google.com/go/firestore"
	firebase "firebase.google.com/go/v4"

	"google.golang.org/api/option"
)

var ctx context.Context
var client *firestore.Client

// SetUp sets up the database
func SetUp() {
	// Initialization
	ctx = context.Background()

	// Connect to Firebase with the service account key
	opt := option.WithCredentialsFile("./API/serviceAccountKey.json")
	app, err := firebase.NewApp(context.Background(), nil, opt)
	if err != nil {
		var errorMsg debug.Debug
		errorMsg.Update(
			http.StatusInternalServerError,
			"database.SetUp() -> Connect to Firebase",
			err.Error(),
			"Unknown",
		)
		return
	}

	client, err = app.Firestore(ctx)
	if err != nil {
		var errorMsg debug.Debug
		errorMsg.Update(
			http.StatusInternalServerError,
			"database.SetUp() -> Create client",
			err.Error(),
			"Unknown",
		)
		return
	}

	defer client.Close()
}
