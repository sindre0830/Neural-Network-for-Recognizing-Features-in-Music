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
    const [filter, setFilter] = useState("")
    const [approved, setApproved] = useState(true)
    const [pending, setPending] = useState(true)

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

    // filter between approved and pending songs
    let filteredSongs;
    if (filter === 'A') {
        filteredSongs = songs.filter(song => song.approved)
    } else if (filter ==='P') {
        filteredSongs = songs.filter(song => !song.approved)
    } else {
        filteredSongs = songs;
    }

    /*if (approved && !pending) {
        filteredSongs = songs.filter(song => song.apporved);
    } else if (!approved && pending) {
        filteredSongs = songs.filter(song => !song.apporved);
    } else {
        filteredSongs = songs;
    }*/

    return (
        <div className='songs'>
            <div className='songs__sort'>
                <input type='search' placeholder='Search for something...' value={search} onChange={(e) => setSearch(e.target.value)}></input>
                <p>Filter:</p>
                <button className='songs__sort-approved' onClick={() => { setFilter('A') }} />
                <p>Approved</p>
                <hr />
                <button className='songs__sort-pending' onClick={() => { setFilter('P') }} />
                <p>Pending</p>
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
