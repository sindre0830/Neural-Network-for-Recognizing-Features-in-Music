package database

import (
	"context"
	"log"

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
		// TODO: proper error handling
		log.Fatalln(err)
	}

	client, err = app.Firestore(ctx)
	if err != nil {
		// TODO: error
		log.Fatalln(err)
	}

	defer client.Close()
}
