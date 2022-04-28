import React, { useState, useEffect } from 'react';
import { FiChevronDown, FiChevronUp } from 'react-icons/fi';
import './song.css';
import SongTitle from '../SongTitle/SongTitle';

const CHORDS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'Cm', 'C#m', 'Dm', 'D#m', 'Em', 'Fm', 'F#m', 'Gm', 'G#m', 'Am', 'A#m', 'Bm'];

/**
 *  Check if the array only contains numbers.
 * 
 *  @param {array} list
 *  @returns {{bool, array}} True if the array only contains numbers.
 */
const checkNumbers = (list) => {
    let obj = {
        flag: true,
        beats: []
    };

    list.forEach(element => {
        let num = parseFloat(element);
        if (isNaN(num)) {
            obj.flag = false;
        }
        obj.beats.push(num);
    });
    return obj;
}

/**
 *  Check if the array only conatins valid chords.
 * 
 *  @param {array} list
 *  @returns {bool} True if the array only contains chords.
 */
const checkChords = (list) => {
    let flag = true;
    list.forEach(element => {
        if (!CHORDS.includes(element)) {
            flag = false;
        }
    });
    return flag;
}

/**
 *  Displaying of one song.
 */
const Song = (props) => {
    const [toggleSong, setToggle] = useState(false);
    const [message, setMessage] = useState("");
    const [title, setTitle] = useState("");
    const [bpm, setBpm] = useState(0);
    const [beats, setBeats] = useState("");
    const [chords, setChords] = useState("");
    const [approved, setApproved] = useState(props.value.Approved);

    /**
     *  Update result.
     * 
     *  @param {event} e 
     */
    const handleSubmit = async (e) => {
        e.preventDefault();
        let items = {Approved: false};
        // only send the values that have been changed
        if (title !== "") {
            items.Title = title;
        }
        if (bpm !== 0) {
            const num = parseFloat(bpm);
            if (isNaN(num)) {
                setMessage('Not a valid Bpm format');
                return;
            }
            items.Bpm = num;
        }
        if (beats !== "") {
            const beatsSplit = beats.replace(/\s+/g, '').split(",");
            const obj = checkNumbers(beatsSplit);
            if (!obj.flag) {
                setMessage('Not a valid Beats format');
                return;
            }
            items.Beats = obj.beats;
        }
        if (chords !== "") {
            items.Chords = chords.replace(/\s+/g, '').split(",");
            // make sure there are actual chords
            if (!checkChords(items.Chords)) {
                setMessage('Not a valid Chords format');
                return;
            }
        }

        try {
            const options = {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(items)
            }

            const res = await fetch('/v1/results?id=' + props.value.id, options);
            if (res.status === 200) {
                setMessage("Song approved");
                //setApproved(prev => !prev)
            } else {
                setMessage("Something went wrong...");
            }
        } catch (err) {
            console.log(err);
        }
    }

    useEffect(() => {
        setApproved(props.value.Approved)
    }, [props.value.Approved]);

    return (
        <div className='song'>
            <div className='song__bar'>
                <div className='song__bar-title'>
                    <SongTitle title={props.value.Title} status={approved ? 'approved' : 'pending'}/>
                </div>

                {/* show approve button if the song is pending */}
                {!approved &&
                    <button type='submit' form='update'>Approve</button>
                }

                <div className='song__bar-button'>
                    {/* check if song is opened or not */}
                    {toggleSong
                        ? <FiChevronUp data-testid='arrow-up' size={28} onClick={() => setToggle(prev => !prev)} style={{cursor: 'pointer'}}/>
                        : <FiChevronDown data-testid='arrow-down' size={28} onClick={() => setToggle(prev => !prev)} style={{ cursor: 'pointer'}}/>
                    }
                </div>
            </div>
            <div className='song__line'>
                <hr />
                <p><strong>{message}</strong></p>
            </div>
            <div className='song__result'>
                <form className={toggleSong ? 'shown' : 'hidden'} id='update' onSubmit={handleSubmit}>
                    <div className='song__result-group'>
                        <label htmlFor='title'>Title</label>
                        <input type='text' name='title' onChange={(e) => setTitle(e.target.value)} defaultValue={props.value.Title} disabled={approved} />
                    </div>
                    <div className='song__result-group'>
                        <label htmlFor='bpm'>Bpm</label>
                        <input type='text' name='bpm' onChange={(e) => setBpm(e.target.value)} defaultValue={props.value.Bpm} disabled={approved} />
                    </div>
                    <div className='song__result-group'>
                        <label htmlFor='beats'>Beats</label>
                        <input type='text' name='beats' onChange={(e) => setBeats(e.target.value)} defaultValue={props.value.Beats} disabled={approved} />
                    </div>
                    <div className='song__result-group'>
                        <label htmlFor='chords'>Chords</label>
                        <input type='text' name='chords' onChange={(e) => setChords(e.target.value)} defaultValue={props.value.Chords} disabled={approved} />
                    </div>
                </form>
            </div>
        </div>
    )
}

export default Song;
