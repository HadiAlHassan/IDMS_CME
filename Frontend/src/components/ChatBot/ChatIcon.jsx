import React, { useState, Fragment } from "react";
import ChatIcon from "@mui/icons-material/Chat";
import Box from "@mui/material/Box";
import { Fab } from "@mui/material";
import ChatScreen from "./ChatScreen";
import classes from "./ChatIcon.module.css";

function FloatingActionButton() {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  const handleClose = () => {
    setIsChatOpen(false);
  };

  return (
    <Fragment>
      <Box className={classes.floatingActionButtonContainer}>
        <Fab
          className={classes.floatingActionButton}
          aria-label="chat"
          onClick={toggleChat}
        >
          <ChatIcon className={classes.floatingActionIcon} />
        </Fab>
      </Box>
      <ChatScreen open={isChatOpen} handleClose={handleClose} />
    </Fragment>
  );
}

export default FloatingActionButton;
