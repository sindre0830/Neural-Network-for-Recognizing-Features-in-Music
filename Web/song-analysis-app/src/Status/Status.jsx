import React, { useState, useEffect } from 'react';
import './status.css';
import StatusList from '../StatusList/StatusList';

const titles = ["How To Be a Heartbreaker - MARINA", "När vi två blir en - Gyllene Tider", "This is the day - The the"];

/**
 *  Displaying of application status.
 */
const Status = () => {
    const [status, setStatus] = useState([])
    const [isLoading, setLoading] = useState(false)
    const [isError, setError] = useState(false)

    /**
     *  Get application status.
     */
    const getStatus = async () => {
        setLoading(true);
        setError(false);

        console.log("hei");

        try {
            const res = await fetch('/v1/diag');
            const json = await res.json();
            setStatus(json);
        } catch (err) {
            setError(true);
        }
        
        setLoading(false);
    }

    useEffect(() => {
        getStatus()
    }, [])

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