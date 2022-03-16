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
                <h1>{props.value.title}</h1>

                {/* show approve button if the song is pending */}
                {!props.value.approved &&
                    <button>Approve</button>
                }

                {/* check if the arrow is going to point up or down*/}
                {toggleSong
                    ? <FiChevronUp size={28} onClick={() => setToggle(false)} style={{cursor: 'pointer'}}/>
                    : <FiChevronDown size={28} onClick={() => setToggle(true)} style={{ cursor: 'pointer' }}/>
                }
            </div>
            <div className='song__line'>
                <hr />
            </div>
            <div className='song__result'>
                {/* display result */}
                {toggleSong &&
                    <div>
                        <form>
                            <div className='song__result-group'>
                                <label for='title'>Title</label>
                                <input type='text' id='title' name='title' defaultValue={props.value.title} disabled={props.value.approved}/>
                            </div>
                            <div className='song__result-group'>
                                <label for='link'>Link</label>
                                <input type='text' id='link' name='link' defaultValue={props.value.link} disabled={props.value.approved}/>
                            </div>
                            <div className='song__result-group'>
                                <label for='bpm'>Bpm</label>
                                <input type='text' id='bpm' name='bpm' defaultValue={props.value.bpm} disabled={props.value.approved}/>
                            </div>
                            <div className='song__result-group'>
                                <label for='beats'>Beats</label>
                                <input type='text' id='beats' name='beats' defaultValue={props.value.beats} disabled={props.value.approved}/>    
                            </div>
                            <div className='song__result-group'>    
                                <label for='chords'>Chords</label>
                                <input type='text' id='chords' name='chords' defaultValue={props.value.chords} disabled={props.value.approved}/>
                            </div>
                        </form>
                    </div>
                }
            </div>
        </div>
    )
}

export default Song;
