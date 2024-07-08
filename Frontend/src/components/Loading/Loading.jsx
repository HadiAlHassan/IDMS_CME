import React from "react";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";
import classes from "./Loading.module.css";

const Loading = ({ text }) => {
  return (
    <Box className={classes.loadingContainer}>
      <CircularProgress className={classes.loadingSpinner} size={24} />
      <span>{text}</span>
    </Box>
  );
};

export default Loading;
