import React from "react";
import './songTitle.css';

/**
 *  Dislaying of song title.
 */
const SongTitle = (props) => {
    return (
        <div className='song-title'>
            <hr className={`song-title__${props.status}`}/>
            <h1>{props.title}</h1>
        </div>
    )
}

export default SongTitle;