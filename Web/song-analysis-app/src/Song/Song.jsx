import React, { useState } from 'react';
import { FiChevronDown, FiChevronUp } from 'react-icons/fi';
import './song.css';

/**
 *  Displaying of one song.
 */
const Song = (props) => {
    const [toggleSong, setToggle] = useState(false);
    const [title, setTitle] = useState("")
    const [bpm, setBpm] = useState(null)
    const [beats, setBeats] = useState("")
    const [chords, setChords] = useState("")

    /**
     *  Update result.
     * 
     *  @param {event} e 
     */
    const handleSubmit = async (e) => {
        // only send the values that has been changed
        let items = {approved: true};

        if (title !== "") {
            items.title = title;
        }

        if (bpm !== null) {
            items.bpm = parseInt(bpm);
        }

        if (beats !== "") {
            items.beats = beats.replace(/\s+/g, '').split(",");
        }

        if (chords !== "") {
            items.chords = chords.replace(/\s+/g, '').split(",");
        }

        try {
            const options = {
                method: 'PUT',
                body: JSON.stringify(items)
            }

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
                    <button type='submit' form='update'>Approve</button>
                }

                {/* check if the arrow is going to point up or down*/}
                {toggleSong
                    ? <FiChevronUp size={28} onClick={() => setToggle(false)} style={{cursor: 'pointer'}}/>
                    : <FiChevronDown size={28} onClick={() => setToggle(true)} style={{ cursor: 'pointer'}}/>
                }
            </div>
            <div className='song__line'>
                <hr />
            </div>
            <div className='song__result'>
                {/* display result */}
                {toggleSong &&
                    <div>
                        <form id='update' onSubmit={handleSubmit}>
                            <div className='song__result-group'>
                                <label htmlFor='title'>Title</label>
                                <input type='text' id='title' name='title' onChange={(e) => setTitle(e.target.value)} defaultValue={props.value.title} disabled={props.value.approved}/>
                            </div>
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
                        </form>
                    </div>
                }
            </div>
        </div>
    )
}

export default Song;
