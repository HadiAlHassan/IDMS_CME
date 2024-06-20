import Modal from "@mui/material/Modal";
import classes from "./ViewPdfModal.module.css";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import MultipleSelectNative from "./Select";
import styles from "./Select.module.css";
import { Button } from "@mui/material";
import { useState } from "react";
import axios from "axios";
import PdfViewer from "./PdfViewer";
//import { BrowserRouter, Route, Switch } from "react-router-dom";
function ViewPdfModal(props) {
  const handleClose = () => props.setOpen(false);

  const [selectedPdfs, setSelectedPdfs] = useState([]);

  const handleSelectionChange = (newSelection) => {
    setSelectedPdfs(newSelection); // Directly set the state with the current selection
  };

  const handleViewPdf = async () => {
    try {
      const response = await axios.post(
        "http://localhost:8000/api/handle-selected-pdfs",
        { selectedPdfs }
      );
      const pdfUrls = response.data.pdfUrls;
      console.log("PDF URLs:", pdfUrls);
      pdfUrls.forEach((url) => {
        console.log("Opening PDF:", url);
        window.open(url, "_blank");
        //window.open(<PdfViewer fileUrl={url} />, "_blank");
        // <div>
        //   <div>
        //     <Switch>
        //       <Route path={"/" + url}>
        //         <PdfViewer fileUrl={url} />
        //       </Route>
        //     </Switch>
        //   </div>
        // </div>;
      });

      console.log(
        "Successfully sent selected PDFs to the backend:",
        response.data
      );
    } catch (error) {
      console.error("Error sending selected PDFs to the backend:", error);
    }
    setSelectedPdfs([]);
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
export default ViewPdfModal;
