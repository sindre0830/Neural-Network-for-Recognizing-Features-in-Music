import React, { useState, useEffect } from 'react';
import './status.css';
import StatusList from '../StatusList/StatusList';

/**
 *  Displaying of application status.
 */
const Status = () => {
    const [status, setStatus] = useState([])
    const [isLoading, setLoading] = useState(false)

    useEffect(() => {
        // flag used to check if component is mounted or not
        let unmounted = false;
        // get the status of the rest of the program
        const getStatus = async () => {
            setLoading(true);
            try {
                const res = await fetch('/v1/diag');
                const json = await res.json();
                // only set the state if the component is mounted
                if (!unmounted) {
                    setStatus(json);
                }
            } catch (err) {
                console.log(err);
            }
            setLoading(false);
        }
        getStatus();
        // cleanup
        return () => {
            unmounted = true;
        }
    }, []);

    return (
        <div className='status'>
            {isLoading && <p id='error'>Loading...</p>}
            <div className='status__list'>
                <StatusList  title='Processing Songs' value={status.ProcessingSongs ? status.ProcessingSongs : []} status='processing' />
            </div>
            <div className='status__list'>
                <StatusList title='Failed Songs' value={status.FailedSongs ? status.FailedSongs : []} status='failed' />
            </div>
            <div className='status__list'>
                <StatusList title='API Status' value={status.ModelConnection ? ['API Connection: 200', `Model Connection: ${status.ModelConnection}`] : ['API Connection: 500']} />
            </div>
        </div>
    )
}

export default Status;