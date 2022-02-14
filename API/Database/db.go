package database

import (
	"context"
	debug "main/Debug"
	"net/http"

	"cloud.google.com/go/firestore"
	firebase "firebase.google.com/go/v4"

	"google.golang.org/api/option"
)

type Database struct {
	ctx    context.Context
	client *firestore.Client
}

// SetUp sets up the database
func (db *Database) SetUp() {
	// Initialization
	db.ctx = context.Background()

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

	db.client, err = app.Firestore(db.ctx)
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

	defer db.client.Close()
}
