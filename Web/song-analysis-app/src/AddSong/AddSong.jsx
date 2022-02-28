import React, { useState } from 'react';
import './addSong.css';

/**
 * Input page.
 */
const AddSong = () => {
    const [link, setLink] = useState("");
    const [message, setMessage] = useState("");

    let submitLink = async (e) => {
        e.preventDefault();
        try {
            const options = {
                method: 'POST',
                body: JSON.stringify(link)
            }

            const res = await fetch('/post', options);
            if (res.status === 200) {
                setLink("");
                setMessage("Link successfully parsed, result will be uploaded to the result page.");
            } else {
                setLink("");
                setMessage("Error when parsing link");
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
                    : null
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
