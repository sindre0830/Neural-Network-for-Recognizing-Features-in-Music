import React, { useState } from 'react';
import './navbar.css';

const Menu = () => (
    <>
        <ul>
            <li><a>Add song</a> </li>
            <li><a>Results</a></li>
            <li><a>Status</a> </li>
        </ul>
    </>
)

const Navbar = () => {
    const [toggleMenu, setToggleMenu] = useState(false);
    return (
        <div>
            <div>
                <h1>Neural Network for Recognizing Features in Music</h1>
            </div>
            <div>
                {toggleMenu
                    ? <button onClick={() => setToggleMenu(false)}>Close</button>
                    : <button onClick={() => setToggleMenu(true)}>Open</button>}
                {toggleMenu && (
                    <div>
                        <Menu />
                    </div>
                )}
            </div>
        </div>
    )
};

export default Navbar;
