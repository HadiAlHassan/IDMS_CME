import React from "react";
import { useLocation } from "react-router-dom";
import classes from "./PdfViewer.module.css";

const PdfViewer = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const pdfUrl = queryParams.get("url");
  const metadata = JSON.parse(queryParams.get("metadata"));

  return (
    <div className={classes.viewerContainer}>
      <div className={classes.metadataContainer}>
        <h3>Metadata</h3>
        <table className={classes.metadataTable}>
          <tbody>
            {Object.entries(metadata).map(([key, value]) => (
              <tr key={key}>
                <td className={classes.metadataKey}>{key}</td>
                <td className={classes.metadataValue}>{value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className={classes.pdfViewerContainer}>
        <iframe
          src={pdfUrl}
          className={classes.pdfDocument}
          height="100%"
          width="100%"
        ></iframe>
      </div>
    </div>
  );
};

export default PdfViewer;
