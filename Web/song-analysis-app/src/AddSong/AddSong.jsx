import React, { useState } from 'react';
import './addSong.css';

/**
 *  Check if the input is a URL.
 * 
 *  @param {text} link
 *  @returns {Boolean} True if the link is valid.
 */
const validateInput = (link) => {
    if (link.startsWith('https://www.youtube.com/watch?v=') || link.startsWith('https://youtu.be/')) {
        return true;
    }
    return false;
}

/**
 *  Input of YouTube link.
 */
const AddSong = () => {
    const [link, setLink] = useState("");
    const [message, setMessage] = useState("");

    /**
     *  Send the link to the API.
     * 
     *  @param {event} e
     */
    const submitLink = async (e) => {
        e.preventDefault();
        setMessage("Parsing link...");

        // validate link
        if (!validateInput(link)) {
            setMessage("Not a valid link");
            return;
        }

        const item = { link: link }

        try {
            const options = {
                method: 'POST',
                body: JSON.stringify(item)
            }

            const res = await fetch('/v1/analysis', options);

            if (res.status === 200) {
                setLink("");
                setMessage("Song successfully analyzed, the result is uploaded to the results page");
            } else {
                setLink("");
                setMessage("Error when analyzing song");
            }
        } catch (err) {
            console.log(err);
        }
    }

    return (
        <div className='add-song'>
            {/* this is were error/status messages will show up */}
            <div className='add-song__message'>
                {message
                    ? <p>{message}</p>
                    : <br></br>
                }
            </div>
            <div className='add-song__input'>
                <form onSubmit={submitLink}>
                    <input type='text' name='link' placeholder='Input YouTube link...' onChange={(e) => setLink(e.target.value)}/>
                    <button type='submit'>Submit</button>
                </form>
            </div>            
        </div>
    )
};

export default AddSong;
