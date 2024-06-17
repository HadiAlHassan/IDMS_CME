import { Button } from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
function AddPdf() {
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
    } catch (error) {
      console.error("Error uploading file:", error);
    }
    console.log("Selected file:", file);
  }

  return (
    <div>
      <Button
        style={{
          borderRadius: 10,
          backgroundColor: "#1769aa",
          padding: "10px",
          fontSize: "13px",
        }}
        variant="contained"
        startIcon={<CloudUploadIcon />}
        onClick={clickHandler}
      >
        Add PDF
      </Button>
    </div>
  );
}

export default AddPdf;
