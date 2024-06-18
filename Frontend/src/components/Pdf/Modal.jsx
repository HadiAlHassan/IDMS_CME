import Modal from "@mui/material/Modal";
import classes from "./Modal.module.css";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import MultipleSelectNative from "./Select";
import styles from "./Select.module.css";
import { Button } from "@mui/material";
import { useState } from "react";
function BasicModal(props) {
  const handleClose = () => props.setOpen(false);

  const [selectedPdfs, setSelectedPdfs] = useState([]);

  const handleSelectionChange = (newSelection) => {
    setSelectedPdfs(newSelection); // Directly set the state with the current selection
  };

  const handleViewPdf = async () => {
    try {
      const response = await fetch(
        "http://localhost:8000/api/handle-selected-pdfs",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ selectedPdfs }),
        }
      );

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const result = await response.json();
      console.log("Successfully sent selected PDFs to the backend:", result);
    } catch (error) {
      console.error("Error sending selected PDFs to the backend:", error);
    }
    handleClose();
  };

  return (
    <div className="Modal Container">
      <Modal
        open={props.open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <div className="Open Modal Container">
          <form className={classes.form}>
            <IconButton className={classes.actions} onClick={handleClose}>
              <CloseIcon />
            </IconButton>
            <div className="Search Bar">
              <p>
                <label htmlFor="search">Search for a PDF</label>
                <input
                  type="text"
                  id="pdfname"
                  value={props.searchInput}
                  onChange={(userSearch) =>
                    props.setSearchInput(userSearch.target.value)
                  }
                />
              </p>
            </div>
            <div className="Multiple Select Container">
              <MultipleSelectNative
                className={styles.formControl}
                searchInput={props.searchInput}
                id="select-multiple-native"
                onSelectionChange={handleSelectionChange}
              />
            </div>
            <Button
              className={classes.button}
              variant="contained"
              onClick={handleViewPdf}
            >
              VIEW PDF
            </Button>
          </form>
        </div>
      </Modal>
    </div>
  );
}
export default BasicModal;
