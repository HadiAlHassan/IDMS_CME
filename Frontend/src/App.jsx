import Header from "./components/Header/Header";
import AddPdf from "./components/AddPdfButton";



function App() {
  return (
    <div>
      <Header />
      <div style={{ marginTop: "20px" }}>
        <AddPdf/>
      </div>

    </div>
    
  );
}

export default App;
