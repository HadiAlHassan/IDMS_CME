import React, { forwardRef, Fragment, useState } from "react";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import Slide from "@mui/material/Slide";
import TextField from "@mui/material/TextField";
import axios from "axios";
import classes from "./ChatScreen.module.css";

const Transition = forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

export default function ChatScreen({ open, handleClose }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (input.trim() !== "") {
      const newMessages = [...messages, { text: input, isUser: true }];
      setMessages(newMessages);
      setInput("");

      try {
        const response = await axios.post(
          "http://localhost:8000/api/chat-bot",
          {
            query: input,
            chat_history: newMessages,
          }
        );
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: response.data.response, isUser: false },
        ]);
      } catch (error) {
        console.error("Error communicating with backend:", error);
      }
    }
  };

  return (
    <Fragment>
      <Dialog
        open={open}
        TransitionComponent={Transition}
        keepMounted
        onClose={handleClose}
        aria-describedby="chat-dialog-description"
        hideBackdrop={true}
        classes={{ paper: classes.dialogPaper }}
      >
        <DialogTitle>{"AI Legal Assistant"}</DialogTitle>
        <DialogContent>
          <div className={classes.chatContainer}>
            <div className={classes.messagesContainer}>
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={
                    message.isUser
                      ? classes.userMessage
                      : classes.assistantMessage
                  }
                >
                  {message.text}
                </div>
              ))}
            </div>
            <TextField
              className={classes.textField}
              variant="outlined"
              placeholder="Ask me a question..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === "Enter") {
                  handleSend();
                }
              }}
            />
          </div>
        </DialogContent>
        <DialogActions>
          <Button
            sx={{ backgroundColor: "#1769aa" }}
            variant="contained"
            onClick={handleClose}
          >
            Close
          </Button>
          <Button
            sx={{ backgroundColor: "#1769aa" }}
            variant="contained"
            onClick={handleSend}
            color="primary"
          >
            Send
          </Button>
        </DialogActions>
      </Dialog>
    </Fragment>
  );
}
