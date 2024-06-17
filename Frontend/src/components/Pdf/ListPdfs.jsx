import * as React from "react";
import { useState } from "react";
import Button from "@mui/material/Button";
import SearchIcon from "@mui/icons-material/Search";
import BasicModal from "./Modal";
import MultipleSelectNative from "./Select";
function ListPdfs() {
  const [modalOpen, setModalOpen] = useState(false);
  const [searchInput, setSearchInput] = useState("");
  return (
    <div>
      <Button
        style={{
          borderRadius: 10,
          backgroundColor: "#1769aa",
          padding: "10px",
          fontSize: "13px",
        }}
        variant="contained"
        startIcon={<SearchIcon />}
        onClick={() => setModalOpen(true)}
      >
        List PDFs
      </Button>
      <BasicModal
        open={modalOpen}
        setOpen={setModalOpen}
        setSearchInput={setSearchInput}
        searchInput={searchInput}
      >
        <MultipleSelectNative searchInput={searchInput} />
      </BasicModal>
    </div>
  );
}
export default ListPdfs;
