import React from "react";
import Header from "../Header/Header";
import classes from "./ProfilePage.module.css";
import { Box, Typography, Button } from "@mui/material";
const Profile = () => {
  return (
    <>
      <Header />
      <Box className={classes.profileContainer}>
        <img className={classes.avatar} alt="User Name" src="avatar.png" />
        <Typography className={classes.name}>Hello Mr/Mrs</Typography>
        <Typography className={classes.email}>
          {localStorage["email"]}
        </Typography>
      </Box>
    </>
  );
};

export default Profile;
