import React, { useState, useEffect } from 'react';
import './songs.css';
import Song from '../Song/Song';
import '../testData.json';


/**
 *  Displaying of all analyzed songs.
 */
const Songs = () => {
    const [songs, setSongs] = useState([])
    const [isLoading, setLoading] = useState(false)
    const [isError, setError] = useState(false)
    const [search, setSearch] = useState("")
    const [filter, setFilter] = useState("All")

    useEffect(() => {
        // flag used to check if component is mounted or not
        let unmounted = false;
        // get all results
        const getSongs = async () => {
            setLoading(true);
            setError(false);
            try {
                const res = await fetch('localhost:8080/v1/results');
                const json = await res.json();
                if (!unmounted) {
                    setSongs(json);
                }
            } catch (err) {
                console.log(err);
                setError(true);
            }
            setLoading(false);
        }
        getSongs()
        // cleanup
        return () => {
            unmounted = true;
        }
    }, [])

    /**
     *  Filter songs based on search query and filters.
     * 
     *  @returns {Array} Filtered songs.
     */
    const filterSongs = () => {
        // filter based on search query
        let filteredSongs = songs.filter(song => song.title.toLowerCase().includes(search.toLowerCase()));

        // filter based on status
        if (filter === 'Approved') {
            return filteredSongs.filter(song => song.approved);
        } else if (filter === 'Pending') {
            return filteredSongs.filter(song => !song.approved);
        }

        return filteredSongs;
    }
    
    return (
        <div className='songs'>
            <div className='songs__sort'>
                <div className='songs__sort-search'>
                    <input type='search' placeholder='Search for something...' value={search} onChange={(e) => setSearch(e.target.value)}></input>
                </div>
                <div className='songs__sort-filter'>
                    <div className='songs__sort-filter-option'>  
                        <input id='all' type='radio' name='filter' value='all' onClick={() => setFilter("All")} />
                        <label htmlFor='all'>All</label>
                    </div>
                    <div className='songs__sort-filter-option'>
                        <input id='approved' type='radio' name='filter' value='approved' onClick={() => setFilter("Approved")} />
                        <label htmlFor='approved'>Approved</label>
                    </div>
                    <div className='songs__sort-filter-option'>
                        <input id='pending' type='radio' name='filter' value='pending' onClick={() => setFilter("Pending")} />
                        <label htmlFor='pending'>Pending</label>
                    </div>
                </div>
            </div>
            <div className='songs__list'>
                {/* display messages for users if results are loading or something went wrong */}
                {isLoading && <p className='error'>Results are loading...</p>}
                {isError && <p className='error'>Something went wrong...</p>}
                {/* render song components. if there are no songs in the database, display a message for users */}
                {songs
                    ? 
                    <>
                        {filterSongs().map((song, index) => (
                            <Song value={song} key={index} />
                        ))}
                    </>
                    : <p id='error'>No songs have been added yet...</p>
                }   
            </div>
        </div>
    )
};

export default Songs;
