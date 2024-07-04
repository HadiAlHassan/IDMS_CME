import React from "react";
import classes from "./Header.module.css";
import LogoutButton from "../LogOutButton/LogoutButton";

function Header() {
  return (
    <div className={classes.Header}>
      <p className={classes.TitleWebsite}>Intelligent Data Management System</p>
      <LogoutButton />
    </div>
  );
}

export default Header;
