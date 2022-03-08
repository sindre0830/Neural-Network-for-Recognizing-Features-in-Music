import React, { useState } from 'react';
import { FiChevronDown, FiChevronUp } from 'react-icons/fi';
import './song.css';

/**
 *  Displaying of one song.
 */
const Song = (props) => {
    const [toggleSong, setToggle] = useState(false);
    return (
        <div className='song'>
            <div className='song__title'>
                <hr className={props.value.approved ? 'song__title-approved' : 'song__title-pending'} />
                <h1>{props.value.name}</h1>

                {/* show approve button if the song is pending */}
                {!props.value.approved &&
                    <button>Approve</button>
                }

                {/* checks if the arrow is going to point up or down*/}
                {toggleSong
                    ? <FiChevronUp size={28} onClick={() => setToggle(false)} style={{cursor: 'pointer'}}/>
                    : <FiChevronDown size={28} onClick={() => setToggle(true)} style={{ cursor: 'pointer' }}/>
                }
            </div>
            <hr />
            <div className='song__result'>
                {/* displays result */}
                {toggleSong &&
                    <div>
                        <pre>{JSON.stringify(props.value, null, 2)}</pre>
                    </div>
                }
            </div>
        </div>
    )
}

export default Song;
