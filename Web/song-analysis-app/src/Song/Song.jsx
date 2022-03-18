import React, { useState } from 'react';
import { FiChevronDown, FiChevronUp } from 'react-icons/fi';
import './song.css';

/**
 *  Displaying of one song.
 */
const Song = (props) => {
    const [toggleSong, setToggle] = useState(false);
    const [title, setTitle] = useState(props.value.title);
    const [bpm, setBpm] = useState(props.value.bpm);
    const [beats, setBeats] = useState(props.value.beats);
    const [chords, setChords] = useState(props.value.chords);

    /**
     *  Update result.
     * 
     *  @param {event} e 
     */
    const handleSubmit = async (e) => {
        console.log(title);

        try {
            const options = {
                method: 'PUT',
                body: JSON.stringify({
                    title: title,
                    bpm: bpm,
                    beats: beats,
                    chords: chords,
                    approved: true
                })
            }
            //let url = "/results" + props.id

            console.log(options.body);

            const res = await fetch('/results', options);
        } catch (err) {
            console.log(err);
        }
    }
 
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
                        <form onSubmit={handleSubmit}>
                            <div className='song__result-group'>
                                <label htmlFor='title'>Title</label>
                                <input type='text' id='title' name='title' onChange={(e) => setTitle(e.target.value)} defaultValue={props.value.title} disabled={props.value.approved}/>
                            </div>
                            {/*<div className='song__result-group'>
                                <label for='link'>Link</label>
                                <input type='text' id='link' name='link' defaultValue={props.value.link} disabled={props.value.approved}/>
                            </div>*/}
                            <div className='song__result-group'>
                                <label htmlFor='bpm'>Bpm</label>
                                <input type='text' id='bpm' name='bpm' onChange={(e) => setBpm(e.target.value)} defaultValue={props.value.bpm} disabled={props.value.approved}/>
                            </div>
                            <div className='song__result-group'>
                                <label htmlFor='beats'>Beats</label>
                                <input type='text' id='beats' name='beats' onChange={(e) => setBeats(e.target.value)} defaultValue={props.value.beats} disabled={props.value.approved}/>    
                            </div>
                            <div className='song__result-group'>    
                                <label htmlFor='chords'>Chords</label>
                                <input type='text' id='chords' name='chords' onChange={(e) => setChords(e.target.value)} defaultValue={props.value.chords} disabled={props.value.approved}/>
                            </div>
                            <button type='submit'>Submit</button>
                        </form>
                    </div>
                }
            </div>
        </div>
    )
}

export default Song;
