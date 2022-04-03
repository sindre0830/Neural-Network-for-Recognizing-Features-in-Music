import React from "react";
import './songTitle.css';

/**
 *  Dislaying of song title.
 */
const SongTitle = (props) => {
    return (
        <div className='song-title'>
            <hr className={`song-title__${props.status}`}/>
            <p>{props.title}</p>
        </div>
    )
}

export default SongTitle;