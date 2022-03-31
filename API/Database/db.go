package database

import (
	"context"

	"cloud.google.com/go/firestore"
	firebase "firebase.google.com/go/v4"

	"google.golang.org/api/iterator"
	"google.golang.org/api/option"
)

// Global object for db connection
var Firestore Database

// Database structure contains db variables
type Database struct {
	Ctx    context.Context
	Client *firestore.Client
}

// Setup sets up the database.
func (db *Database) Setup() error {
	// initialization
	db.Ctx = context.Background()

	// connect to Firebase with the service account key
	opt := option.WithCredentialsFile("./test-aa354-firebase-adminsdk-iktfk-7cd7559143.json")
	app, err := firebase.NewApp(context.Background(), nil, opt)
	if err != nil {
		return err
	}

	db.Client, err = app.Firestore(db.Ctx)
	if err != nil {
		return err
	}

	return nil
}

// Get a document from a collection.
func (db *Database) Get(collection string, id string) (map[string]interface{}, error) {
	// find the document with the specific ID
	dsnap, err := db.Client.Collection(collection).Doc(id).Get(db.Ctx)
	if err != nil {
		return nil, err
	}

	data := dsnap.Data()
	return data, nil
}

// Get all documents from a collection.
func (db *Database) GetAll(collection string, processing bool) ([]map[string]interface{}, error) {
	var data []map[string]interface{}
	var doc map[string]interface{}
	// iterate through collection
	iter := db.Client.Collection(collection).Where("Processing", "==", processing).Documents(db.Ctx)
	for {
		el, err := iter.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			return nil, err
		}
		// get the current document's id
		doc = el.Data()
		doc["id"] = el.Ref.ID
		// add document to data slice
		data = append(data, doc)
	}

	return data, nil
}

// Add a document to a collection.
func (db *Database) Add(collection string, id string, data interface{}) error {
	_, err := db.Client.Collection(collection).Doc(id).Set(db.Ctx, data)
	return err
}

// Update a document.
func (db *Database) Update(collection string, id string, data interface{}) error {
	// check if the ID is a valid document
	_, err := db.Client.Collection(collection).Doc(id).Get(db.Ctx)
	if err != nil {
		// prevents the creation of a new document
		return err
	}

	// update with new data
	_, err = db.Client.Collection(collection).Doc(id).Set(db.Ctx, data, firestore.MergeAll)
	return err
}

// Delete a document from a collection.
func (db *Database) Delete(collection string, id string) error {
	_, err := db.Client.Collection(collection).Doc(id).Delete(db.Ctx)
	return err
}
