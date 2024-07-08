import React from "react";
import classes from "./Header.module.css";
import LogoutButton from "../LogOutButton/LogoutButton";
import SideBarDrawer from "../SideBar/SideBarDrawer";
function Header() {
  return (
    <div className={classes.Header}>
      <LogoutButton />
      <p className={classes.TitleWebsite}>Intelligent Data Management System</p>
      <SideBarDrawer />
    </div>
  );
}

export default Header;
