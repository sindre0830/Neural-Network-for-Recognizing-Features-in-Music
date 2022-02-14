package database

import (
	"context"

	"cloud.google.com/go/firestore"
	firebase "firebase.google.com/go/v4"

	"google.golang.org/api/iterator"
	"google.golang.org/api/option"
)

// Database structure contains db variables
type Database struct {
	ctx    context.Context
	client *firestore.Client
}

// Setup sets up the database.
func (db *Database) Setup() error {
	// initialization
	db.ctx = context.Background()

	// connect to Firebase with the service account key
	opt := option.WithCredentialsFile("./serviceAccountKey.json")
	app, err := firebase.NewApp(context.Background(), nil, opt)
	if err != nil {
		return err
	}

	db.client, err = app.Firestore(db.ctx)
	if err != nil {
		return err
	}

	return nil
}

// Get a document from a collection.
func (db *Database) Get(collection string, id string) (map[string]interface{}, error) {
	// find the document with the specific ID
	dsnap, err := db.client.Collection(collection).Doc(id).Get(db.ctx)
	if err != nil {
		return nil, err
	}

	data := dsnap.Data()
	return data, nil
}

// Get all documents from a collection.
func (db *Database) GetAll(collection string) ([]map[string]interface{}, error) {
	var data []map[string]interface{}
	// iterate through collection
	iter := db.client.Collection(collection).Documents(db.ctx)
	for {
		el, err := iter.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			return nil, err
		}
		// add current document to the data slice
		data = append(data, el.Data())
	}
	return data, nil
}

// Add a document to a collection.
func (db *Database) Add(collection string, id string, data interface{}) error {
	_, err := db.client.Collection(collection).Doc(id).Set(db.ctx, data)
	return err
}

// Delete a document from a collection.
func (db *Database) Delete(collection string, id string) error {
	_, err := db.client.Collection(collection).Doc(id).Delete(db.ctx)
	return err
}
