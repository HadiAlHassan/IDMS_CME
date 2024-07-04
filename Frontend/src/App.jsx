import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./HomePage";
import PdfViewer from "./components/Pdf/PdfViewer";
import SignIn from "./components/SignInPage/SignIn";
import SignUp from "./components/SignUpPage/Signup"; // Corrected casing
import PrivateRoute from "./routes/PrivateRoute";
import "./index.css";
import { AuthProvider } from "./components/Context/AuthContext";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="App">
          <Routes>
            <Route path="/" element={<SignIn />} />
            <Route path="/signup" element={<SignUp />} />
            <Route
              path="/homepage"
              element={<PrivateRoute element={HomePage} />}
            />
            <Route
              path="/view-pdf"
              element={<PrivateRoute element={PdfViewer} />}
            />
          </Routes>
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
