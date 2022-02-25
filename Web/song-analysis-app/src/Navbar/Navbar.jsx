import React from 'react';
import './navbar.css';

const Navbar = () => {
    return (
        <div>
            <div>
                <h1>Neural Network for Recognizing Features in Music</h1>
            </div>
            <div>
                <ul>
                    <li><a>Add song</a> </li>
                    <li><a>Results</a></li> 
                    <li><a>Status</a> </li>
                </ul>
            </div>
        </div>
    )
};

export default Navbar;
