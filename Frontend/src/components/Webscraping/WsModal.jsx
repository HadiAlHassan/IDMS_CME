import * as React from "react";
import PropTypes from "prop-types";
import clsx from "clsx";
import { styled, css } from "@mui/system";
import { Modal as BaseModal } from "@mui/base/Modal";
import FeedIcon from "@mui/icons-material/Feed";
import Button from "@mui/material/Button";
import classes from "./WsModal.module.css";
import TextField from "@mui/material/TextField";
import axios from "axios";
import SuccessAlerts from "../Alert/Success";
import ErrorAlerts from "../Alert/Error";
import { useContext, useState } from "react";
import { UpdateContext } from "../Context/UpdateContext";
import Loading from "../Loading/Loading";
import { faIR } from "@mui/material/locale";

export default function WebScrapingModal() {
  const [showSuccessAlert, setShowSuccessAlert] = useState(false);
  const [showErrorAlert, setShowErrorAlert] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const { handleFileUploadSuccess } = useContext(UpdateContext);
  const [open, setOpen] = React.useState(false);
  const [loading, setLoading] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => {
    setOpen(false);
  };

  async function handleScrape() {
    console.log(
      "Scraping website:",
      document.getElementById("urlToScrape").value
    );
    setLoading(true);
    handleClose();
    try {
      const response = await axios.post(
        "http://localhost:8000/api/scrape-website",
        {
          url: document.getElementById("urlToScrape").value,
        }
      );
      console.log("Scraped website:", response.data);
      setShowSuccessAlert(true);
      setTimeout(() => setShowSuccessAlert(false), 5000);
      handleFileUploadSuccess(); // Call this to update the word cloud
    } catch (error) {
      console.error("Error scraping website:", error);
      setShowErrorAlert(true);
      setErrorMessage(error.response?.data?.error);
      setTimeout(() => setShowErrorAlert(false), 5000);
    } finally {
      setLoading(false); // Set loading to false after the scraping process is complete
    }
  }

  return (
    <div>
      <Button
        className={classes.scrapeWesbiteButton}
        variant="contained"
        startIcon={<FeedIcon />}
        onClick={handleOpen}
      >
        Scrape a website
      </Button>
      {loading && <Loading text={"Analyzing your URL"} />}
      <Modal
        aria-labelledby="unstyled-modal-title"
        aria-describedby="unstyled-modal-description"
        open={open}
        onClose={handleClose}
        slots={{ backdrop: StyledBackdrop }}
      >
        <ModalContent className={classes.modalContainer}>
          <Button
            variant="contained"
            onClick={handleClose}
            sx={{
              borderRadius: "50%",
              minWidth: "40px",
              minHeight: "40px",
              padding: "0",
              position: "absolute",
              top: "0.5rem",
              right: "0.5rem",
            }}
          >
            X
          </Button>
          <h3>Scrape a website</h3>
          <TextField id="urlToScrape" label="URL" variant="outlined" />
          <Button
            className={classes.scrapeButton}
            variant="contained"
            onClick={handleScrape}
          >
            Scrape
          </Button>
        </ModalContent>
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

const Backdrop = React.forwardRef((props, ref) => {
  const { open, className, ...other } = props;
  return (
    <div
      className={clsx({ "base-Backdrop-open": open }, className)}
      ref={ref}
      {...other}
    />
  );
});

Backdrop.propTypes = {
  className: PropTypes.string.isRequired,
  open: PropTypes.bool,
};

const blue = {
  200: "#99CCFF",
  300: "#66B2FF",
  400: "#3399FF",
  500: "#007FFF",
  600: "#0072E5",
  700: "#0066CC",
};

const grey = {
  50: "#F3F6F9",
  100: "#E5EAF2",
  200: "#DAE2ED",
  300: "#C7D0DD",
  400: "#B0B8C4",
  500: "#9DA8B7",
  600: "#6B7A90",
  700: "#434D5B",
  800: "#303740",
  900: "#1C2025",
};

const Modal = styled(BaseModal)`
  position: fixed;
  z-index: 1300;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const StyledBackdrop = styled(Backdrop)`
  z-index: -1;
  position: fixed;
  inset: 0;
  background-color: rgb(0 0 0 / 0.5);
  -webkit-tap-highlight-color: transparent;
`;

const ModalContent = styled("div")(
  ({ theme }) => css`
    font-family: "IBM Plex Sans", sans-serif;
    font-weight: 500;
    text-align: start;
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 8px;
    overflow: hidden;
    background-color: ${theme.palette.mode === "dark" ? grey[900] : "#fff"};
    border-radius: 8px;
    border: 1px solid ${theme.palette.mode === "dark" ? grey[700] : grey[200]};
    box-shadow: 0 4px 12px
      ${theme.palette.mode === "dark" ? "rgb(0 0 0 / 0.5)" : "rgb(0 0 0 / 0.2)"};
    padding: 24px;
    color: ${theme.palette.mode === "dark" ? grey[50] : grey[900]};

    & .modal-title {
      margin: 0;
      line-height: 1.5rem;
      margin-bottom: 8px;
    }

    & .modal-description {
      margin: 0;
      line-height: 1.5rem;
      font-weight: 400;
      color: ${theme.palette.mode === "dark" ? grey[400] : grey[800]};
      margin-bottom: 4px;
    }
  `
);
