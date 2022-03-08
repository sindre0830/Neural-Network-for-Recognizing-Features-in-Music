import React from 'react';
import './song.css';

/**
 *  Result from one song.
 */
const Song = (props) => {
    return (
        <div className='song'>
            <h1>{props.value.name}</h1>
            <hr />
        </div>
    )
}

export default Song;
