import React from "react";
import AddPdf from "./components/Pdf/AddPdf";
import ListPdfs from "./components/Pdf/ListPdfs";
import WebScrapButton from "./components/Webscraping/WebScrapButton";
import Dashboard from "./components/Dashboard/Dashboard";
import { Container } from "@mui/material";
import "./index.css";

function HomePage() {
  return (
    <div className="Homepage">
      <Container>
        <div className="flexContainer">
          <div className="addPdfContainer">
            <AddPdf />
          </div>
          <div className="viewPdfContainer">
            <ListPdfs />
          </div>
          <div className="WebScrapContainer">
            <WebScrapButton />
          </div>
        </div>
        <div className="dashboard">
          <Dashboard />
        </div>
      </Container>
    </div>
  );
}
export default HomePage;
