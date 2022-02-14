package database

import (
	"context"
	debug "main/Debug"
	"net/http"

	"cloud.google.com/go/firestore"
	firebase "firebase.google.com/go/v4"

	"google.golang.org/api/iterator"
	"google.golang.org/api/option"
)

type Database struct {
	ctx    context.Context
	client *firestore.Client
}

// Setup sets up the database.
func (db *Database) Setup() {
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

// Get a document from a collection.
func (db *Database) Get(collection string, id string) (map[string]interface{}, error) {
	// Find the document with the specific ID
	dsnap, err := db.client.Collection(collection).Doc(id).Get(db.ctx)
	if err != nil {
		return nil, err
	}

	data := dsnap.Data()
	return data, err
}

// Get all documents from a collection.
func (db *Database) GetAll(collection string) ([]map[string]interface{}, error) {
	var data []map[string]interface{}
	// Iterate through collection
	iter := db.client.Collection(collection).Documents(db.ctx)
	for {
		el, err := iter.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			return nil, err
		}
		// Add current document to the data slice
		data = append(data, el.Data())
	}
	return data, nil
}

// Add a document to a collection.
func (db *Database) Add(collection string, id string, data interface{}) error {
	_, err := db.client.Collection(collection).Doc(id).Set(db.ctx, data)
	if err != nil {
		return err
	}
	return nil
}
