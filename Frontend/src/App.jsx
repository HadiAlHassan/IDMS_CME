import Header from "./components/Header/Header";
import AddPdf from "./components/Pdf/AddPdf";
import ListPdfs from "./components/Pdf/ListPdfs";
import "./index.css";

function App() {
  return (
    <div>
      <Header />
      <div className="flexContainer">
        <div className="addPdfContainer">
          <AddPdf/>
        </div>
        <div>
          <ListPdfs/> 
        </div>
      </div>
    </div>
  );
}

export default App;