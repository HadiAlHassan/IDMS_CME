import * as React from "react";
import { useState } from "react";
import Button from "@mui/material/Button";
import SearchIcon from "@mui/icons-material/Search";
import BasicModal from "./Modal";
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
