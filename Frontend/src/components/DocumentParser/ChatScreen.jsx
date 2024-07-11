import React, { useState, forwardRef, Fragment } from "react";
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Slide,
  TextField,
} from "@mui/material";
import axios from "axios";
import classes from "./ChatScreen.module.css";

const Transition = forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

const ChatScreen = ({ open, handleClose, title }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (input.trim() !== "") {
      const newMessages = [...messages, { text: input, isUser: true }];
      setMessages(newMessages);
      setInput("");

      try {
        console.log(title);
        const response = await axios.post("http://localhost:8000/api/rag", {
          query: input,
          chat_history: newMessages,
          title: title,
        });
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
        <DialogTitle>{"Document Chatbot"}</DialogTitle>
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
              placeholder="Ask me a question about your documents"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleSend();
                }
              }}
            />
          </div>
        </DialogContent>
        <DialogActions>
          <Button
            variant="contained"
            onClick={handleClose}
            className={classes.closeButton}
          >
            Close
          </Button>
          <Button
            variant="contained"
            onClick={handleSend}
            className={classes.sendButton}
          >
            Send
          </Button>
        </DialogActions>
      </Dialog>
    </Fragment>
  );
};

export default ChatScreen;
