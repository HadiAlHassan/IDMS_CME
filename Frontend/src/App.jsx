import Header from "./components/Header/Header";
import "./index.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./HomePage";
import PdfViewer from "./components/Pdf/PdfViewer";
import SignIn from "./SignIn";
import PrivateRoute from "./routes/PrivateRoute";
function App() {
  return (
    <BrowserRouter>
      <Header />
      <div className="App">
        <Routes>
          <Route exact path="/" element={<SignIn />} />
          <Route
            exact
            path="/homepage"
            element={<PrivateRoute element={HomePage} />}
          />
          <Route
            exact
            path="/view-pdf"
            element={<PrivateRoute element={PdfViewer} />}
          />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
