import { Button } from "@mui/material";
import classes from "./WebScrapButton.module.css";
import FeedIcon from "@mui/icons-material/Feed";
import { useState } from "react";
import WebScrapingModal from "./WebScrapingModal";

function WebScrapButton() {
  const [modalOpen, setModalOpen] = useState(false);
  return (
    <div className="WebScrapButton Container">
      <Button
        className={classes.button}
        variant="contained"
        startIcon={<FeedIcon />}
        onClick={() => setModalOpen(true)}
      >
        Scrape a website
      </Button>
      <WebScrapingModal
        open={modalOpen}
        setOpen={setModalOpen}
      ></WebScrapingModal>
    </div>
  );
}
export default WebScrapButton;
