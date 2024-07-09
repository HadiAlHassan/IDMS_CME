import React from "react";
import AddPdf from "./components/Pdf/AddPdf";
import WebScrapingModal from "./components/Webscraping/WsModal";
import Dashboard from "./components/Dashboard/Dashboard";
import FloatingActionButton from "./components/ChatBot/ChatIcon";
import BasicModal from "./components/Pdf/Modal";
import { UpdateProvider } from "./components/Context/UpdateContext";
import { Container } from "@mui/material";
import "./index.css";
import Header from "./components/Header/Header";
import SideBarDrawer from "./components/SideBar/SideBarDrawer";

function HomePage() {
  return (
    <UpdateProvider>
      <div className="Homepage">
        <Header />
        <Container>
          <div className="flexContainer">
            <div className="addPdfContainer">
              <AddPdf />
            </div>
            <div className="viewPdfContainer">
              <BasicModal />
            </div>
            <div className="WebScrapContainer">
              <WebScrapingModal />
            </div>
          </div>
          <div className="dashboard">
            <Dashboard />
          </div>
        </Container>
        <FloatingActionButton />
      </div>
    </UpdateProvider>
  );
}
export default HomePage;
