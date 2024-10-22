import Header from "./components/Header/Header";
import "./index.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./HomePage";
import PdfViewer from "./components/Pdf/PdfViewer";

function App() {
  return (
    <BrowserRouter>
      <Header />
      <div className="App">
        <Routes>
          <Route exact path="/" element={<HomePage />}></Route>
          <Route exact path="/view-pdf" element={<PdfViewer />}></Route>
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
