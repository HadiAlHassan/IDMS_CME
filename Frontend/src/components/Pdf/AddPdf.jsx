import { Button } from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import classes from "./AddPdf.module.css";
import SuccessAlerts from "../Alert/Success";
import { useState } from "react";

function AddPdf() {
  const [showSuccessAlert, setShowSuccessAlert] = useState(false);

  function clickHandler() {
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = ".pdf";
    fileInput.click();
    fileInput.addEventListener("change", fileSelectHandler);
  }

  async function fileSelectHandler(event) {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/api/add-pdf", {
        method: "POST",
        body: formData,
      });
      const result = await response.json();
      console.log("Server response:", result);
      setShowSuccessAlert(true);
      setTimeout(() => setShowSuccessAlert(false), 5000);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
    console.log("Selected file:", file);
  }

  return (
    <div className={classes.container}>
      <Button
        className={classes.button}
        variant="contained"
        startIcon={<CloudUploadIcon />}
        onClick={clickHandler}
      >
        Add PDF
      </Button>
      <SuccessAlerts
        open={showSuccessAlert}
        message="PDF uploaded successfully"
        onClose={() => setShowSuccessAlert(false)}
      />
    </div>
  );
}

export default AddPdf;
