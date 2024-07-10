import React, { useState } from "react";
import {
  Modal,
  Box,
  Typography,
  TextField,
  Button,
  Menu,
  MenuItem,
} from "@mui/material";
import classes from "./EditCaseModal.module.css";

const EditCaseModal = ({ open, onClose, caseItem, onSave }) => {
  const [caseName, setCaseName] = useState(caseItem.caseName);
  const [clientName, setClientName] = useState(caseItem.clientName);
  const [caseStatus, setCaseStatus] = useState(caseItem.caseStatus);
  const [openedDate, setOpenedDate] = useState(caseItem.openedDate);
  const [trialDates, setTrialDates] = useState(caseItem.trialDates.join(", "));
  const [documents, setDocuments] = useState(caseItem.documents.join(", "));

  const handleSave = () => {
    const updatedCase = {
      ...caseItem,
      caseName,
      clientName,
      caseStatus,
      openedDate,
      trialDates: trialDates.split(", "),
      documents: documents.split(", "),
    };
    onSave(updatedCase);
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Box className={classes.modalBox}>
        <Typography variant="h6" gutterBottom>
          Edit Case
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
          <MenuItem value="Closed">Closed</MenuItem>
          <MenuItem value="Pending">Pending</MenuItem>
        </TextField>
        <TextField
          label="Opened Date"
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
          value={trialDates}
          onChange={(e) => setTrialDates(e.target.value)}
          fullWidth
          margin="normal"
          InputLabelProps={{
            shrink: true,
          }}
        />
        <TextField
          label="Documents"
          value={documents}
          onChange={(e) => setDocuments(e.target.value)}
          fullWidth
          margin="normal"
          helperText="Comma separated values"
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

export default EditCaseModal;
