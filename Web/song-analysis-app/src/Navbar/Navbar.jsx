import React, { useState } from 'react';
import { FiMenu, FiX } from 'react-icons/fi'; 
import './navbar.css';

const Menu = () => (
    <>
        <ul>
            <li>Add song</li>
            <li>Results</li>
            <li>Status</li>
        </ul>
    </>
)

const Navbar = () => {
    const [toggleMenu, setToggle] = useState(false);
    return (
        <div className='navbar'>
            <div className='navbar__title'>
                <h1>Neural Network for Recognizing Features in Music</h1>
            </div>
            <div className='navbar__links'>
                <Menu />
            </div>
            <div className='navbar__menu'>
                {toggleMenu
                    ? <FiX size={32} onClick={() => setToggle(false)}/>
                    : <FiMenu size={32} onClick={() => setToggle(true)}/> }
                {toggleMenu && (
                    <div className='navbar__menu-links'>
                        <Menu />
                    </div>
                )}
            </div>
            
        </div>
    )
};

export default Navbar;
