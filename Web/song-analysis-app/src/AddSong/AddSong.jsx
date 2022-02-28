import React from 'react';
import './addSong.css';

/**
 * Input page.
 */
const AddSong = () => {
    return (
        <div className='add-song'>
            {/* this is were error/status messages will show up */}
            <div className='add-song__message'>
                <p>Hei</p>
            </div>
            <div className='add-song__input'>
                <form>
                    <input type='text' name='link' placeholder='Input YouTube link...'/>
                    <button>Submit</button>
                </form>
            </div>            
        </div>
    )
};

export default AddSong;
