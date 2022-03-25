import React, { useState, useEffect } from 'react';
import './songs.css';
import Song from '../Song/Song';
import '../testData.json';


/**
 *  Displaying of all analyzed songs.
 */
const Songs = () => {
    const [songs, fetchSongs] = useState([])
    const [search, setSearch] = useState("")
    const [filter, setFilter] = useState("All")

    /**
     *  Get results from the API.
     */
    const getSongs = () => {
        /*const jsonData= require('../testData.json'); 
        fetchSongs(jsonData);*/

        try {
            fetch('/v1/results')
            .then((res) => res.json())
            .then((res) => {
            console.log(res)
            fetchSongs(res)
            })
        } catch (err) {
            console.log("hei")
            console.log(err)
        }
    }

    useEffect(() => {
        getSongs()
    }, [])

    /**
     *  Filter songs based on search query and filters.
     * 
     *  @returns {Array} Filtered songs.
     */
    const filterSongs = () => {
        // filter based on search query
        let filteredSongs = songs.filter(song => song.Title.toLowerCase().includes(search.toLowerCase()));

        // filter based on status
        if (filter === 'Approved') {
            return filteredSongs.filter(song => song.Approved);
        } else if (filter === 'Pending') {
            return filteredSongs.filter(song => !song.Approved);
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
                        <input type='radio' name='filter' value='all' onClick={() => setFilter("All")} />
                        <label htmlFor='all'>All</label>
                    </div>
                    <div className='songs__sort-filter-option'>
                        <input type='radio' name='filter' value='approved' onClick={() => setFilter("Approved")} />
                        <label htmlFor='approved'>Approved</label>
                    </div>
                    <div className='songs__sort-filter-option'>
                        <input type='radio' name='filter' value='pending' onClick={() => setFilter("Pending")} />
                        <label htmlFor='pending'>Pending</label>
                    </div>
                </div>
            </div>
            <div className='songs__list'>
                {/* render the song components
                    if there are no songs in the database, render a message for the user */}
                {songs !== null
                    ? 
                    <>
                        {filterSongs().map((song, index) => (
                            <Song value={song} key={index} />
                        ))}
                    </>
                    : <p>No songs have been added yet...</p>
                }
                
            </div>
        </div>
    )
};

export default Songs;
