import React, { useState } from 'react';
import { FiChevronDown, FiChevronUp } from 'react-icons/fi';
import './songStatus.css';
import SongTitle from '../SongTitle/SongTitle';

const SongStatus = (props) => {
    const [toggle, setToggle] = useState(true);

    return (
        <div className='song-status'>
            <div className='song-status__bar'>
                <h1>{props.title}</h1>
                {/* check if list is going to be displayed or not */}
                {toggle
                    ? <FiChevronUp size={28} onClick={() => setToggle(prev => !prev)} style={{cursor: 'pointer'}}/>
                    : <FiChevronDown size={28} onClick={() => setToggle(prev => !prev)} style={{ cursor: 'pointer'}}/>
                }
            </div>

            {/* render all titles if list is supposed to be displayed */}
            {toggle &&
                <>
                    {props.value.map((song, index) => (
                    <div className='song-status__title'>
                        <SongTitle title={song} status={props.status} />
                        <hr id='line'/>
                    </div>
                ))}
                </> 
            }
            
        </div>
    )
}

export default SongStatus;