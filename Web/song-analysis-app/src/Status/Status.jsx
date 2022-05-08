import React, { useState, useEffect } from 'react';
import './status.css';
import StatusList from '../StatusList/StatusList';

/**
 *  Displaying of application status.
 */
const Status = () => {
    const [status, setStatus] = useState([])
    const [isLoading, setLoading] = useState(true)

    const getStatus = async () => {
        // flag used to check if component is mounted or not
        let unmounted = false;
        // get the status of the rest of the program
        const getStatus = async () => {
            try {
                const res = await fetch('/v1/diag');
                // only set the state if the component is mounted
                if (res.status === 200 && !unmounted) {
                    const json = await res.json();
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
    }

    useEffect(() => {
        const timer = setInterval(getStatus, 2000);
        return () => clearInterval(timer);
    }, []);

    return (
        <div className='status'>
            {isLoading && <p id='error'>Loading...</p>}
            <div className='status__list'>
                <StatusList  title='Processing Songs' value={status.processing_songs ? status.processing_songs : []} status='processing' />
            </div>
            <div className='status__list'>
                <StatusList title='Failed Songs' value={status.failed_songs ? status.failed_songs : []} status='failed' />
            </div>
            <div className='status__list'>
                <StatusList title='API Status' value={status.model_connection ? ['API Connection: 200', `Model Connection: ${status.model_connection}`] : ['API Connection: 500']} />
            </div>
        </div>
    )
}

export default Status;