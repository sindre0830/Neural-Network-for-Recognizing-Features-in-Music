import React, { useState } from 'react';
import { FiChevronDown, FiChevronUp } from 'react-icons/fi';
import './statusList.css';
import SongTitle from '../SongTitle/SongTitle';

/**
 *  List of status.
 */
const StatusList = (props) => {
    const [toggle, setToggle] = useState(true);

    return (
        <div className='status-list'>
            <div className='status-list__bar'>
                <h1>{props.title}</h1>
                {/* check if list is going to be displayed or not */}
                {toggle
                    ? <FiChevronUp title='arrow-down' size={28} onClick={() => setToggle(prev => !prev)} style={{cursor: 'pointer'}}/>
                    : <FiChevronDown title='arrow-up' size={28} onClick={() => setToggle(prev => !prev)} style={{ cursor: 'pointer'}}/>
                }
            </div>

            {/* render all titles if list is supposed to be displayed */}
            {toggle &&
                <>
                    {props.value.map((song, index) => (
                        <div className='status-list__title'>
                            <SongTitle title={song} status={props.status} key={index} />
                            {/* create a line between each title */}
                            {index+1 !== props.value.length &&
                                <hr id='line'/>
                            }
                        </div>
                ))}
                </> 
            }
            
        </div>
    )
}

export default StatusList;