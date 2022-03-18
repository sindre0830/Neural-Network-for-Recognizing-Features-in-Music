import React, { useState, useEffect } from 'react';
import './songs.css';
import Song from '../Song/Song';
import '../testData.json';


/**
 *  Displaying of all analyzed songs.
 */
const Songs = () => {
    const [songs, fetchSongs] = useState([])

    /**
     *  Get results from the API.
     */
    const getSongs = () => {
        {/*const jsonData= require('../testData.json'); 
        fetchSongs(jsonData);*/}

        try {
            fetch('/results')
            .then((res) => res.json())
            .then((res) => {
            console.log(res)
            fetchSongs(res)
            })
        } catch (err) {
            console.log(err)
        }
    }

    useEffect(() => {
        getSongs()
    }, [])

    return (
        <div className='songs'>
            <div className='songs__sort'>
                <input placeholder='Search for something...' type='text'></input>
                <p>Filter:</p>
                <div className='songs__sort-approved' />
                <p>Approved</p>
                <hr />
                <div className='songs__sort-pending' />
                <p>Pending</p>
            </div>
            <div className='songs__list'>
                {songs.map( (song, index) => (
                    <Song value={song} key={index} />
                ))}
            </div>
        </div>
    )
};

export default Songs;
