import React from "react";
import { useLocation, Navigate } from "react-router-dom";
import classes from "./PdfViewer.module.css";

const PdfViewer = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const pdfUrl = queryParams.get("url");
  const metadata = JSON.parse(queryParams.get("metadata"));

  const formatKey = (key) => {
    return key
      .replace(/_/g, " ") // Replace underscores with spaces
      .replace(/\b\w/g, (char) => char.toUpperCase()); // Capitalize first letter of each word
  };

  const formatValue = (value) => {
    if (typeof value === "object" && !Array.isArray(value)) {
      return (
        <table className={classes.nestedTable}>
          <tbody>
            {Object.entries(value).map(([subKey, subValue]) => (
              <tr key={subKey}>
                <td className={classes.metadataKey}>{formatKey(subKey)}</td>
                <td className={classes.metadataValue}>
                  {Array.isArray(subValue)
                    ? subValue.join(", ")
                    : subValue.toString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      );
    }
    if (Array.isArray(value)) {
      return value.join(", ");
    }
    return value.toString();
  };

  const formatMetadata = (data) => {
    return Object.entries(data).map(([key, value]) => (
      <tr key={key}>
        <td className={classes.metadataKey}>{formatKey(key)}</td>
        <td className={classes.metadataValue}>{formatValue(value)}</td>
      </tr>
    ));
  };

  return (
    <div className={classes.viewerContainer}>
      <div className={classes.metadataContainer}>
        <h3>Metadata</h3>
        <table className={classes.metadataTable}>
          <tbody>
            <tr>
              <th colSpan="2" className={classes.metadataSectionTitle}>
                General Info
              </th>
            </tr>
            {formatMetadata(metadata.general_info)}
            <tr>
              <th colSpan="2" className={classes.metadataSectionTitle}>
                NLP Analysis
              </th>
            </tr>
            {formatMetadata(metadata.nlp_analysis)}
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
