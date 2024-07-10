import React, { useState } from "react";
import {
  Modal,
  Box,
  Typography,
  TextField,
  Button,
  MenuItem,
} from "@mui/material";
import axios from "axios";
import classes from "./EditCaseModal.module.css";
import Tags from "./MultipleAutoComplete";
import { useNavigate } from "react-router-dom"; // Import useNavigate hook

const EditCaseModal = ({ open, onClose, caseItem, onSave }) => {
  const [newName, setNewName] = useState(caseItem.name || "");
  const [clientName, setClientName] = useState(caseItem.client || "");
  const [caseStatus, setCaseStatus] = useState(caseItem.status || "");
  const [openedDate, setOpenedDate] = useState(caseItem.time || "");
  const [trialDate, setTrialDate] = useState(caseItem.trial_date || "");
  const [selectedDocuments, setSelectedDocuments] = useState(
    caseItem.documents_related || []
  );
  const navigate = useNavigate(); // Initialize useNavigate hook

  const handleSave = async () => {
    try {
      const updatedCase = {
        name: caseItem.name, // current name used to find the case
        user_id: localStorage["firebase_id"], // Replace with actual user ID
      };

      // Only include fields that have been changed
      if (newName !== caseItem.name) updatedCase.new_name = newName;
      if (clientName !== caseItem.client) updatedCase.client = clientName;
      if (caseStatus !== caseItem.status) updatedCase.status = caseStatus;
      if (openedDate !== caseItem.time) updatedCase.time = openedDate;
      if (trialDate !== caseItem.trial_date) updatedCase.trial_date = trialDate;
      if (selectedDocuments !== caseItem.documents_related)
        updatedCase.document_titles = selectedDocuments;
      const response = await axios.put(
        "http://localhost:8000/api/update-case",
        updatedCase
      );

      if (response.status === 200) {
        console.log("Case updated successfully:", response.data);
        navigate("/cases");

        onSave(updatedCase);
        onClose();
        // Reroute to /cases after successful update
      } else {
        console.error("Error updating case:", response.data);
      }
    } catch (error) {
      console.error("Error updating case:", error);
    }
  };

  return (
    <div>
      <Modal open={open} onClose={onClose}>
        <Box className={classes.modalBox}>
          <Typography variant="h6" gutterBottom>
            Edit Case
          </Typography>
          <TextField
            label="New Case Name"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
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
            <MenuItem value="Closed">Closed</MenuItem>
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
          <Tags
            selectedDocuments={selectedDocuments}
            setSelectedDocuments={setSelectedDocuments}
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
    </div>
  );
};

export default EditCaseModal;
