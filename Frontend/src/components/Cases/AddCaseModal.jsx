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
import classes from "./AddCaseModal.module.css";
import SuccessAlerts from "../Alert/Success";
import ErrorAlerts from "../Alert/Error";

const AddCaseModal = ({ open, onClose, addCase }) => {
  const [caseName, setCaseName] = useState("");
  const [clientName, setClientName] = useState("");
  const [caseStatus, setCaseStatus] = useState("");
  const [openedDate, setOpenedDate] = useState("");
  const [trialDate, setTrialDate] = useState("");
  const [showSuccessAlert, setShowSuccessAlert] = useState(false);
  const [showErrorAlert, setShowErrorAlert] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleSave = async () => {
    try {
      const newCase = {
        name: caseName,
        client: clientName,
        status: caseStatus,
        time: openedDate,
        trial_date: trialDate,
        user_id: localStorage["firebase_id"], // You should replace this with the actual user ID
      };

      const response = await axios.post(
        "http://localhost:8000/api/create-case",
        newCase
      );
      if (response.status === 201) {
        console.log("Case created successfully:", response.data);
        setShowSuccessAlert(true);
        setTimeout(() => setShowSuccessAlert(false), 5000);
        addCase(newCase);
        onClose();
      } else {
        setShowErrorAlert(true);
        setErrorMessage(response.data.error || "Error creating case");
        setTimeout(() => setShowErrorAlert(false), 5000);
        console.error("Error creating case:", response.data);
      }
    } catch (error) {
      setShowErrorAlert(true);
      setErrorMessage(error.response?.data?.error || "Error creating case");
      setTimeout(() => setShowErrorAlert(false), 5000);
      console.error("Error creating case:", error);
    }
  };

  return (
    <div>
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
      <SuccessAlerts
        open={showSuccessAlert}
        message="Case created successfully"
        onClose={() => setShowSuccessAlert(false)}
      />
      <ErrorAlerts
        open={showErrorAlert}
        message={errorMessage}
        onClose={() => setShowErrorAlert(false)}
      />
    </div>
  );
};

export default AddCaseModal;
