import { Button } from "@mui/material";
import classes from "./DocInfoButton.module.css";
import FeedIcon from "@mui/icons-material/Feed";
import { useState } from "react";

function clickHandler() {
  console.log("Doc Metadata button clicked");
}
function DocInfoButton() {
  const [modalOpen, setModalOpen] = useState(false);
  const [searchInput, setSearchInput] = useState("");
  return (
    <div className="DocInfoButton Container">
      <Button
        className={classes.button}
        variant="contained"
        startIcon={<FeedIcon />}
        // onClick={() => setModalOpen(true)}
      >
        Doc Metadata
      </Button>
    </div>
  );
}
export default DocInfoButton;
