import * as React from "react";
import { useState } from "react";
import Button from "@mui/material/Button";
import SearchIcon from "@mui/icons-material/Search";
import ViewPdfModal from "./ViewPdfModal";
import MultipleSelectNative from "./Select";
import classes from "./ListPdfs.module.css";
function ListPdfs() {
  const [modalOpen, setModalOpen] = useState(false);
  const [searchInput, setSearchInput] = useState("");
  return (
    <div>
      <Button
        className={classes.button}
        variant="contained"
        startIcon={<SearchIcon />}
        onClick={() => setModalOpen(true)}
      >
        Look for PDFs
      </Button>
      <ViewPdfModal
        open={modalOpen}
        setOpen={setModalOpen}
        setSearchInput={setSearchInput}
        searchInput={searchInput}
      >
        <MultipleSelectNative searchInput={searchInput} />
      </ViewPdfModal>
    </div>
  );
}
export default ListPdfs;
