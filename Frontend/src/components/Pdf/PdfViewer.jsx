import React from "react";
import { useLocation } from "react-router-dom";
import classes from "./PdfViewer.module.css";
import Header from "../Header/Header";
import ChatIcon from "../DocumentParser/ChatIcon";
const PdfViewer = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const pdfUrl = queryParams.get("url");
  const metadata = JSON.parse(queryParams.get("metadata"));
  const excludedFields = ["_id", "general_info_id", "nlp_id", "document_type"];
  const title = metadata.general_info.title;
  const formatKey = (key) => {
    if (key === "ner") {
      return "Named Entity Recognition";
    }
    return key
      .replace(/_/g, " ") // Replace underscores with spaces
      .replace(/\b\w/g, (char) => char.toUpperCase()); // Capitalize first letter of each word
  };

  const formatSpecialValue = (key, value) => {
    if (key === "ner" || key === "references" || key === "in_text_citations") {
      // Remove "OrderedDict" and strip brackets
      const cleanedValue = JSON.stringify(value)
        .replace(/OrderedDict/g, "")
        .replace(/[\{\}\[\]]/g, "")
        .replace(/['"]+/g, "")
        .replace(/: ,/g, ": NONE,")
        .replace(/: $/g, ": NONE");

      return cleanedValue;
    }
    return value.toString();
  };

  const formatValue = (key, value) => {
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
    if (key === "date_submitted") {
      return new Date(value).toISOString().split("T")[0]; // Format date
    }
    return formatSpecialValue(key, value);
  };

  const formatMetadata = (data) => {
    if (!data) return null;
    return Object.entries(data)
      .filter(([key]) => !excludedFields.includes(key))
      .map(([key, value]) => (
        <tr key={key}>
          <td className={classes.metadataKey}>{formatKey(key)}</td>
          <td className={classes.metadataValue}>{formatValue(key, value)}</td>
        </tr>
      ));
  };

  return (
    <>
      <Header />
      <div className={classes.pagecontainer}>
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
              title="PDF Viewer"
            ></iframe>
          </div>
        </div>
        <ChatIcon title={title} />
      </div>
    </>
  );
};

export default PdfViewer;
