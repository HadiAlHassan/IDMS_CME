import React from 'react';
import classes from './Header.module.css';

function Header() {
    return (
      <div className = {classes.Header}>
        <p className = {classes.TitleWebsite}>Intelligent Data Management System</p>
      </div>
    );
  }
  
  export default Header;