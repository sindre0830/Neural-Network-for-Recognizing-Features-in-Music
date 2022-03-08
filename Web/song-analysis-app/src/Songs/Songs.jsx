import React, { useState, useEffect } from 'react';
import './songs.css';

/**
 *  Displaying of all analyzed songs.
 */
const Songs = () => {
    const [Songs, fetchSongs] = useState([])

    const getData = () => {
        fetch('https://jsonplaceholder.typicode.com/users')
        .then((res) => res.json())
        .then((res) => {
            console.log(res)
            fetchSongs(res)
        })
    }

    useEffect(() => {
        getData()
    }, [])

    return (
        <div className='songs'>
            <h2>React Fetch API Example</h2>
            <ul>
                {Songs.map((song, i) => {
                return <li key={i}>{song.name}</li>
                })}
            </ul>
        </div>
    )
};

export default Songs;
