import React, { useState } from "react";
import {
  Modal,
  Box,
  Typography,
  TextField,
  Button,
  MenuItem,
} from "@mui/material";
import classes from "./AddCaseModal.module.css";

const AddCaseModal = ({ open, onClose }) => {
  const [caseName, setCaseName] = useState("");
  const [clientName, setClientName] = useState("");
  const [caseStatus, setCaseStatus] = useState("");
  const [openedDate, setOpenedDate] = useState("");
  const [trialDate, setTrialDate] = useState("");

  const handleSave = () => {
    // Logic to save the new case
    onClose();
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Box className={classes.modalBox}>
        <Typography variant="h6" gutterBottom>
          Add New Case
        </Typography>
        <TextField
          label="Case Name"
          value={caseName}
          onChange={(e) => setCaseName(e.target.value)}
          fullWidth
          margin="normal"
        />
        <TextField
          label="Client Name"
          value={clientName}
          onChange={(e) => setClientName(e.target.value)}
          fullWidth
          margin="normal"
        />
        <TextField
          select
          label="Case Status"
          value={caseStatus}
          onChange={(e) => setCaseStatus(e.target.value)}
          fullWidth
          margin="normal"
        >
          <MenuItem value="Open">Open</MenuItem>
          <MenuItem value="Pending">Pending</MenuItem>
        </TextField>
        <TextField
          label="Open Date"
          type="date"
          value={openedDate}
          onChange={(e) => setOpenedDate(e.target.value)}
          fullWidth
          margin="normal"
          InputLabelProps={{
            shrink: true,
          }}
        />
        <TextField
          label="Trial Date"
          type="date"
          value={trialDate}
          onChange={(e) => setTrialDate(e.target.value)}
          fullWidth
          margin="normal"
          InputLabelProps={{
            shrink: true,
          }}
        />
        <Box mt={2} display="flex" justifyContent="flex-end">
          <Button onClick={onClose} className={classes.cancelButton}>
            Cancel
          </Button>
          <Button
            onClick={handleSave}
            color="primary"
            variant="contained"
            className={classes.saveButton}
          >
            Save
          </Button>
        </Box>
      </Box>
    </Modal>
  );
};

export default AddCaseModal;
