import React, { useState } from 'react';
import { FiMenu, FiX } from 'react-icons/fi';
import { NavLink } from 'react-router-dom';
import './navbar.css';

/** 
 *   Displaying of the menu links.
 */
const Menu = (props) => (
    <>
        <ul>
            <li onClick={props.click}>
                <NavLink className={({isActive}) => (isActive ? 'menu-active' : 'menu')} to='/'>Add song</NavLink>
            </li>
            <li onClick={props.click}>
                <NavLink className={({isActive}) => (isActive ? 'menu-active' : 'menu')} to='results'>Results</NavLink>
            </li>
            <li onClick={props.click}>
                <NavLink className={({isActive}) => (isActive ? 'menu-active' : 'menu')} to='status'>Status</NavLink>
            </li>
        </ul>
    </>
)

/**
 *  Naviagtion bar.
 */
const Navbar = () => {
    const [toggleMenu, setToggle] = useState(false);

    /**
     *  Close the dropdown menu when an item is clicked.
     */
    const handleClick = () => {
        setToggle(prev => !prev);
    }

    return (
        <div className='navbar'>
            <div className='navbar__title'>
                <h1>Neural Network for Recognizing Features in Music</h1>
            </div>
            <div className='navbar__links'>
                <Menu />
            </div>
            {/* div for dropdown menu, only showed on small screens */}
            <div className='navbar__menu'>
                {toggleMenu
                    ? <FiX size={32} onClick={() => setToggle(prev => !prev)} style={{cursor: 'pointer'}} />
                    : <FiMenu size={32} onClick={() => setToggle(prev => !prev)} style={{cursor: 'pointer'}} /> }
                {toggleMenu && (
                    <div className='navbar__menu-links'>
                        <Menu click={handleClick} />
                    </div>
                )}
            </div>
            
        </div>
    )
};

export default Navbar;
