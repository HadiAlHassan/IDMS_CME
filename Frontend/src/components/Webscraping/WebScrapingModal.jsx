import React from "react";
import Modal from "@mui/material/Modal";
import { useState } from "react";
import classes from "./WebScrapingModal.module.css";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import { Button } from "@mui/material";
import axios from "axios";

function WsModal(props) {
  const handleClose = () => props.setOpen(false);
  function handleScrape() {
    console.log(
      "Scraping website:",
      document.getElementById("urlToScrape").value
    );
    axios
      .post("http://localhost:8000/api/scrape-website", {
        url: document.getElementById("urlToScrape").value,
      })

      .then((response) => {
        console.log("Scraped website:", response.data);
      })
      .catch((error) => {
        console.error("Error scraping website:", error);
      });
    handleClose();
  }
  return (
    <div>
      <Modal
        className={classes.modal}
        open={props.open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <form className={classes.form}>
          <IconButton className={classes.actions} onClick={handleClose}>
            <CloseIcon />
          </IconButton>
          <div className="Input URL Bar">
            <p>
              <label htmlFor="Scrape">
                Input the URL of the website you'd like to scrape:
              </label>
              <input type="text" id="urlToScrape" />
            </p>
          </div>

          <Button
            className={classes.button}
            variant="contained"
            onClick={handleScrape}
          >
            Scrape
          </Button>
        </form>
      </Modal>
    </div>
  );
}
export default WsModal;
