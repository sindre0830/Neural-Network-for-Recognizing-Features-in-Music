import React, { useState } from 'react';
import './addSong.css';


/**
 *  Check if the input is a URL.
 * 
 *  @param {text} link
 */
const validateInput = (link) => {
    var regexp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-/]))?/
    return regexp.test(link);
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
