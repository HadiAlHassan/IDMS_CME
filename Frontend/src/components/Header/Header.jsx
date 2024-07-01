import React from "react";
import classes from "./Header.module.css";

function Header() {
  return (
    <div className={classes.Header}>
      <div className={classes.TitleWebsite}>
        <p>Intelligent Data Management System</p>
      </div>
    </div>
  );
}

export default Header;
