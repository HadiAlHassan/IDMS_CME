import { Container } from "@mui/material";
import Header from "./components/Header/Header";
import AddPdf from "./components/Pdf/AddPdf";
import ListPdfs from "./components/Pdf/ListPdfs";
import DocInfoButton from "./components/Doc/DocInfoButton";
import "./index.css";

function App() {
  return (
    <div>
      <Header />
      <Container>
        <div className="flexContainer">
          <div className="addPdfContainer">
            <AddPdf />
          </div>
          <div className="viewPdfContainer">
            <ListPdfs />
          </div>
          <div className="docInfoContainer">
            <DocInfoButton />
          </div>
        </div>
      </Container>
    </div>
  );
}

export default App;
