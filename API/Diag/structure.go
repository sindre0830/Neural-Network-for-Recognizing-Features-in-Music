package diag

// Status stores the applications' status
type Diag struct {
	ModelConnection int
	ProcessingSongs []string
	FailedSongs     []string
}
