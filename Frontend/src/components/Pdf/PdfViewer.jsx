import React, { useState } from "react";
import classes from "./PdfViewer.module.css";

function PdfViewer(props) {
  const File =
    "http://localhost:8000/api/get-pdf-by-id/667316e97bc6fd28f91912d8/";

  return (
    <div className={classes.pdfViewerContainer}>
      <iframe
        //src={props.fileUrl}
        src={File}
        className={classes.pdfDocument}
        height="100%"
        width="100%"
      ></iframe>
    </div>
  );
}

export default PdfViewer;
