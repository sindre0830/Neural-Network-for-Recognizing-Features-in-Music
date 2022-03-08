import React, { useState, useEffect } from 'react';
import './songs.css';
import Song from '../Song/Song';
import '../testData.json';

/**
 *  Displaying of all analyzed songs.
 */
const Songs = () => {
    const [songs, fetchSongs] = useState([])

    const getSongs = () => {
        const jsonData= require('../testData.json'); 
        console.log(jsonData);
        fetchSongs(jsonData);

        {/*try {
            fetch('../testData.json')
            .then((res) => res.json())
            .then((res) => {
            console.log(res)
            fetchSongs(res)
            })
        } catch (err) {
            console.log(err)
        } */}
    }

    useEffect(() => {
        getSongs()
    }, [])

    return (
        <div className='songs'>
            {songs.map( (song, index) => (
                <Song value={song} key={index} />
            ))}
        </div>
    )
};

export default Songs;
