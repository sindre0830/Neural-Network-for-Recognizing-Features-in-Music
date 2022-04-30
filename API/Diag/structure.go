package diag

// Diag stores the applications' status
type Diag struct {
	ModelConnection int      `json:"model_connection"`
	ProcessingSongs []string `json:"processing_songs"`
	FailedSongs     []string `json:"failed_songs"`
}
