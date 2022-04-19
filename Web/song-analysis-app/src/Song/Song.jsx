import React, { useState } from 'react';
import { FiChevronDown, FiChevronUp } from 'react-icons/fi';
import './song.css';
import SongTitle from '../SongTitle/SongTitle';

/**
 *  Displaying of one song.
 */
const Song = (props) => {
    const [toggleSong, setToggle] = useState(false);
    const [title, setTitle] = useState("")
    const [bpm, setBpm] = useState(0)
    const [beats, setBeats] = useState("")
    const [chords, setChords] = useState("")

    /**
     *  Update result.
     * 
     *  @param {event} e 
     */
    const handleSubmit = async (e) => {        
        let items = {Approved: true};
        // only send the values that have been changed
        if (title !== "") {
            items.Title = title;
        }
        if (bpm !== 0) {
            items.Bpm = parseFloat(bpm);
        }
        if (beats !== "") {
            items.Beats = beats.replace(/\s+/g, '').split(",");
        }
        if (chords !== "") {
            items.Chords = chords.replace(/\s+/g, '').split(",");
        }

        try {
            const options = {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(items)
            }

            await fetch('/v1/results?id=' + props.value.id, options);
        } catch (err) {
            console.log(err);
        }
    }
 
    return (
        <div className='song'>
            <div className='song__bar'>
                <div className='song__bar-title'>
                    <SongTitle title={props.value.Title} status={props.value.Approved ? 'approved' : 'pending'}/>
                </div>

                {/* show approve button if the song is pending */}
                {!props.value.Approved &&
                    <button type='submit' form='update'>Approve</button>
                }

                <div className='song__bar-button'>
                    {/* check if song is opened or not */}
                    {toggleSong
                        ? <FiChevronUp size={28} onClick={() => setToggle(prev => !prev)} style={{cursor: 'pointer'}}/>
                        : <FiChevronDown size={28} onClick={() => setToggle(prev => !prev)} style={{ cursor: 'pointer'}}/>
                    }
                </div>
            </div>
            <div className='song__line'>
                <hr />
            </div>
            <div className='song__result'>
                {/* display result */}
                {toggleSong &&
                    <>
                        <form id='update' onSubmit={handleSubmit}>
                            <div className='song__result-group'>
                                <label htmlFor='title'>Title</label>
                                <input type='text' id='title' name='title' onChange={(e) => setTitle(e.target.value)} defaultValue={props.value.Title} disabled={props.value.Approved} />
                            </div>
                            <div className='song__result-group'>
                                <label htmlFor='bpm'>Bpm</label>
                                <input type='text' id='bpm' name='bpm' onChange={(e) => setBpm(e.target.value)} defaultValue={props.value.Bpm} disabled={props.value.Approved} />
                            </div>
                            <div className='song__result-group'>
                                <label htmlFor='beats'>Beats</label>
                                <input type='text' id='beats' name='beats' onChange={(e) => setBeats(e.target.value)} defaultValue={props.value.Beats} disabled={props.value.Approved} />
                            </div>
                            <div className='song__result-group'>
                                <label htmlFor='chords'>Chords</label>
                                <input type='text' id='chords' name='chords' onChange={(e) => setChords(e.target.value)} defaultValue={props.value.Chords} disabled={props.value.Approved} />
                            </div>
                        </form>
                    </>
                }
            </div>
        </div>
    )
}

export default Song;
