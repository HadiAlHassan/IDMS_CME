import React, { useEffect, useState } from "react";
import Autocomplete from "@mui/material/Autocomplete";
import TextField from "@mui/material/TextField";
import axios from "axios";

const Tags = ({ selectedDocuments, setSelectedDocuments }) => {
  const [documentTitles, setDocumentTitles] = useState([]);

  useEffect(() => {
    const fetchDocumentTitles = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8000/api/get-all-titles"
        );
        if (response.status === 200) {
          setDocumentTitles(response.data.titles);
        } else {
          console.error("Failed to fetch document titles:", response.data);
        }
      } catch (error) {
        console.error("Error fetching document titles:", error);
      }
    };

    fetchDocumentTitles();
  }, []);

  return (
    <Autocomplete
      multiple
      id="tags-outlined"
      options={documentTitles}
      getOptionLabel={(option) => option}
      value={selectedDocuments}
      onChange={(event, newValue) => setSelectedDocuments(newValue)}
      filterSelectedOptions
      renderInput={(params) => (
        <TextField
          {...params}
          label="Related Documents"
          placeholder="Select documents"
        />
      )}
    />
  );
};

export default Tags;
