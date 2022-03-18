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
        const jsonData= require('../testData.json'); 
        fetchSongs(jsonData);

        /*try {
            fetch('/results')
            .then((res) => res.json())
            .then((res) => {
            console.log(res)
            fetchSongs(res)
            })
        } catch (err) {
            console.log(err)
        }*/
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
                {filterSongs().map((song, index) => (
                    <Song value={song} key={index} />
                ))}
            </div>
        </div>
    )
};

export default Songs;
