import React, { useState, useEffect } from 'react';
import { FiChevronDown, FiChevronUp, FiTrash2 } from 'react-icons/fi';
import './song.css';
import SongTitle from '../SongTitle/SongTitle';

const CHORDS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'Cm', 'C#m', 'Dm', 'D#m', 'Em', 'Fm', 'F#m', 'Gm', 'G#m', 'Am', 'A#m', 'Bm'];

/**
 *  Check if the array only contains numbers.
 * 
 *  @param {array} list
 *  @returns {{bool, array}} True if the array only contains numbers, and an array with the values parsed to floats.
 */
const checkNumbers = (list) => {
    let obj = {
        flag: true,
        beats: []
    };

    // convert all values to floats
    list.forEach(element => {
        let num = parseFloat(element);
        // make sure the value is a valid float
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
    const [approved, setApproved] = useState(props.value.approved);

    /**
     *  Delete result.
     * 
     *  @param {event} e 
     */
    const handleDelete = async (e) => {
        e.preventDefault();
        setMessage('Deleting song...');

        try {
            const options = {
                method: 'DELETE'
            }

            const res = await fetch('/v1/results?id=' + props.value.id, options);
            if (res.status === 200) {
                setMessage("");
                setApproved(prev => !prev)
                // update the song in the parent component
                props.delete(props.value.id);
            } else {
                setMessage('Something went wrong...');
            }
        } catch (err) {
            console.log(err);
        }
    }

    /**
     *  Update result.
     * 
     *  @param {event} e 
     */
    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage('Updating song...');
        let data = {};
        // if the song is pending, add date from the other fields
        // if not, only the approved label is changed
        if (!approved) {
            data = validateData();
            // if an error message has been written, do not submit the updated result
            if (message !== "") {
                return;
            }
        } else {
            data = {approved: !approved};
        }

        try {
            const options = {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            }

            const res = await fetch('/v1/results?id=' + props.value.id, options);
            if (res.status === 200) {
                setMessage("");
                setApproved(prev => !prev)
                // update the song in the parent component
                props.update(props.value.id);
            } else {
                setMessage('Something went wrong...');
            }
        } catch (err) {
            console.log(err);
        }
    }

    /**
     *  Create an object with validated data.
     * 
     *  @returns {{bool, object}} True if the data is valid, and an object with the validated data.
     */
    const validateData = () => {
        let items = {approved: !approved};
        if (title !== "") {
            items.title = title;
        }
        if (bpm !== 0) {
            const num = parseFloat(bpm);
            if (isNaN(num)) {
                setMessage('Not a valid Bpm format');
                return;
            }
            items.bpm = num;
        }
        if (beats !== "") {
            const beatsSplit = beats.replace(/\s+/g, '').split(",");
            const obj = checkNumbers(beatsSplit);
            if (!obj.flag) {
                setMessage('Not a valid Beats format');
                return;
            }
            items.beats = obj.beats;
        }
        if (chords !== "") {
            items.chords = chords.replace(/\s+/g, '').split(",");
            // make sure there are actual chords
            if (!checkChords(items.chords)) {
                setMessage('Not a valid Chords format');
                return;
            }
        }
        return items;
    }

    useEffect(() => {
        setApproved(props.value.approved)
    }, [props.value.approved]);

    return (
        <div className='song'>
            <div className='song__bar'>
                <div className='song__bar-title'>
                    <SongTitle title={props.value.title} status={approved ? 'approved' : 'pending'}/>
                </div>

                <FiTrash2 size={28} onClick={handleDelete} style={{ cursor: 'pointer' }}/>
                {/* show approve button if the song is pending */}
                {approved
                    ? <button className='song__bar-edit' onClick={handleSubmit}>Edit</button>
                    : <button className='song__bar-approve' type='submit' form={`update-${props.value.id}`} >Approve</button>
                }

                <div className='song__bar-arrow'>
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
                <form className={toggleSong ? 'shown' : 'hidden'} id={`update-${props.value.id}`} onSubmit={handleSubmit}>
                    <div className='song__result-group'>
                        <label htmlFor={`title-${props.value.id}`}>Title</label>
                        <input id={`title-${props.value.id}`} type='text' name='title' onChange={(e) => setTitle(e.target.value)} defaultValue={props.value.title} disabled={approved} />
                    </div>
                    <div className='song__result-group'>
                        <label htmlFor={`bpm-${props.value.id}`}>Bpm (use . for decimal values)</label>
                        <input id={`bpm-${props.value.id}`} type='text' name='bpm' onChange={(e) => setBpm(e.target.value)} defaultValue={props.value.bpm} disabled={approved} />
                    </div>
                    <div className='song__result-group'>
                        <label htmlFor={`beats-${props.value.id}`}>Beats (value1,value2,...valueN)</label>
                        <input id={`beats-${props.value.id}`} type='text' name='beats' onChange={(e) => setBeats(e.target.value)} defaultValue={props.value.beats} disabled={approved} />
                    </div>
                    <div className='song__result-group'>
                        <label htmlFor={`chords-${props.value.id}`}>Chords (value1,value2,...valueN)</label>
                        <input id={`chords-${props.value.id}`} type='text' name='chords' onChange={(e) => setChords(e.target.value)} defaultValue={props.value.chords} disabled={approved} />
                    </div>
                </form>
            </div>
        </div>
    )
}

export default Song;
