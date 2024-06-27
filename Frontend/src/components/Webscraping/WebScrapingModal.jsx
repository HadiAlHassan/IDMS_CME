import React from "react";
import Modal from "@mui/material/Modal";
import { useState } from "react";
import classes from "./WebScrapingModal.module.css";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import { Button } from "@mui/material";
import axios from "axios";
import SuccessAlerts from "../Alert/Success";
import ErrorAlerts from "../Alert/Error";

function WsModal(props) {
  const handleClose = () => props.setOpen(false);
  const [showSuccessAlert, setShowSuccessAlert] = useState(false);
  const [showErrorAlert, setShowErrorAlert] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
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
        setShowSuccessAlert(true);
        setTimeout(() => setShowSuccessAlert(false), 5000);
      })
      .catch((error) => {
        console.error("Error scraping website:", error);
        setShowErrorAlert(true);
        setErrorMessage(error.response?.data?.error);
        setTimeout(() => setShowErrorAlert(false), 5000);
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
      <SuccessAlerts
        open={showSuccessAlert}
        message="Website scraped successfully"
        onClose={() => setShowSuccessAlert(false)}
      />
      <ErrorAlerts
        open={showErrorAlert}
        message={errorMessage}
        onClose={() => setShowErrorAlert(false)}
      />
    </div>
  );
}
export default WsModal;
