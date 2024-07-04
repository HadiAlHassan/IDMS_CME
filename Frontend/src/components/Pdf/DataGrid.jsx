import * as React from "react";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { useState, useEffect } from "react";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";
import axios from "axios";
import { useAuth } from "../Context/AuthContext";
import { useNavigate } from "react-router-dom";

const fetchMetadata = async () => {
  try {
    const response = await fetch("http://localhost:8000/api/get-all-metadata");
    if (!response.ok) {
      throw new Error("Failed to fetch metadata");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching metadata:", error);
    return [];
  }
};

const transformData = (data) => {
  return data.map((item, index) => ({
    id: index + 1,
    title: item.title,
    author: item.author,
    date_submitted: item.date_submitted,
    category: item.category,
    language: item.language,
    confidentiality_level: item.confidentiality_level ? "Yes" : "No",
    word_count: item.word_count,
  }));
};

const columns = [
  { field: "title", headerName: "Title", width: 300 },
  { field: "author", headerName: "Author", width: 200 },
  { field: "date_submitted", headerName: "Date Submitted", width: 200 },
  { field: "category", headerName: "Category", width: 150 },
  { field: "language", headerName: "Language", width: 100 },
  { field: "confidentiality_level", headerName: "Confidential", width: 150 },
  { field: "word_count", headerName: "Word Count", width: 150 },
];

const BasicExampleDataGrid = () => {
  const [data, setData] = useState([]);
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const getData = async () => {
      const metadata = await fetchMetadata();
      setData(transformData(metadata));
    };

    getData();
  }, []);

  const handleRowDoubleClick = async (params) => {
    if (!user) {
      navigate("/");
      return;
    }
    const selectedPdfTitle = params.row.title;

    try {
      const response_pdf = await axios.post(
        "http://localhost:8000/api/handle-selected-pdfs",
        { selectedPdfs: [selectedPdfTitle] }
      );
      const response_metadata = await axios.post(
        "http://localhost:8000/api/get_metadata_by_pdf_name",
        { selectedPdfs: [selectedPdfTitle] }
      );

      const pdfUrl = response_pdf.data.pdfUrls[0];
      const metadata = response_metadata.data.pdf_metadata[0];
      console.log("Metadata:", metadata);
      console.log("PDF URL:", pdfUrl);

      if (!pdfUrl) {
        console.log("No PDF URL returned from the server");
        return;
      }

      // Ensure metadata is an object containing general_info and nlp_analysis keys
      const viewerUrl = `/view-pdf?url=${encodeURIComponent(
        pdfUrl
      )}&metadata=${encodeURIComponent(JSON.stringify(metadata))}`;
      window.open(viewerUrl, "_blank");
    } catch (error) {
      console.error("Error opening PDF:", error);
    }
  };

  return (
    <div style={{ height: 400, width: "100%" }}>
      <DataGrid
        rows={data}
        columns={columns}
        slots={{ toolbar: GridToolbar }}
        onRowDoubleClick={handleRowDoubleClick}
      />
    </div>
  );
};

export default BasicExampleDataGrid;
