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

    // filtering of songs based on status
    let filteredSongs;
    if (filter == 'Approved') {
        filteredSongs = songs.filter(song => song.approved);
    } else if (filter == 'Pending') {
        filteredSongs = songs.filter(song => !song.approved);
    } else {
        filteredSongs = songs;
    }

    return (
        <div className='songs'>
            <div className='songs__filter'>
                {/*<input type='search' placeholder='Search for something...' value={search} onChange={(e) => setSearch(e.target.value)}></input>*/}
                <div className='songs__filter-option'>  
                    <input type='radio' name='filter' value='all' onClick={() => setFilter("All")} />
                    <label for='all'>All</label>
                </div>
                <div className='songs__filter-option'>
                    <input type='radio' name='filter' value='approved' onClick={() => setFilter("Approved")} />
                    <label for='approved'>Approved</label>
                </div>
                <div className='songs__filter-option'>
                    <input type='radio' name='filter' value='pending' onClick={() => setFilter("Pending")} />
                    <label for='pending'>Pending</label>
                </div>
            </div>
            <div className='songs__list'>
                {filteredSongs.map( (song, index) => (
                    <Song value={song} key={index} />
                ))}
            </div>
        </div>
    )
};

export default Songs;
