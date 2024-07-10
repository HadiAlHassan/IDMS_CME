import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Card, CardContent, Typography, Button } from "@mui/material";
import axios from "axios";
import EditIcon from "@mui/icons-material/Edit";
import classes from "./CaseDetailPage.module.css";
import Header from "../Header/Header";
import EditCaseModal from "../Cases/EditCaseModal";

const CaseDetailPage = () => {
  const { name } = useParams();
  const [caseItem, setCaseItem] = useState(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);

  const [updatedCase, setUpdatedCase] = useState(null);

  useEffect(() => {
    const fetchCase = async () => {
      try {
        const userId = localStorage.getItem("firebase_id");
        const response = await axios.post(
          "http://localhost:8000/api/get-case-details",
          {
            name: name,
            user_id: userId,
          }
        );

        const caseData = response.data;
        setCaseItem(caseData);
        setUpdatedCase(caseData);
      } catch (error) {
        console.error("Error fetching case:", error);
      }
    };

    fetchCase();
  }, [name]);

  if (!caseItem) {
    return <div>Case not found</div>;
  }

  const getStatusClass = (status) => {
    if (status === "Open") return classes.openStatus;
    if (status === "Closed") return classes.closedStatus;
    if (status === "Pending") return classes.pendingStatus;
  };

  const handleOpenEditModal = () => {
    setIsEditModalOpen(true);
  };

  const handleCloseEditModal = () => {
    setIsEditModalOpen(false);
  };

  const handleUpdateCase = (updatedCaseData) => {
    setUpdatedCase(updatedCaseData);
    handleCloseEditModal();
  };

  return (
    <>
      <Header />
      <div className={classes.caseDetailContainer}>
        <Card className={classes.caseDetailCard}>
          <CardContent>
            <Typography variant="h5" className={classes.caseTitle}>
              {updatedCase.name}
            </Typography>
            <Typography className={classes.caseDetail}>
              Client: {updatedCase.client}
            </Typography>
            <Typography
              className={`${classes.caseDetail} ${getStatusClass(
                updatedCase.status
              )}`}
            >
              Status: {updatedCase.status}
            </Typography>
            <Typography className={classes.caseDetail}>
              Opened: {new Date(updatedCase.time).toLocaleString()}
            </Typography>
            <Typography className={classes.caseDetail}>
              Important Dates: {updatedCase.trial_date}
            </Typography>
            <Typography className={classes.caseDetail}>
              Related Documents:
              <ul>
                {updatedCase.documents_related.map((doc, index) => (
                  <li key={index}>{doc}</li>
                ))}
              </ul>
            </Typography>
            <Button
              variant="contained"
              color="primary"
              onClick={handleOpenEditModal}
              startIcon={<EditIcon />}
            >
              Edit Case
            </Button>
          </CardContent>
        </Card>
      </div>
      <EditCaseModal
        open={isEditModalOpen}
        onClose={handleCloseEditModal}
        caseItem={updatedCase}
        onSave={handleUpdateCase}
      />
    </>
  );
};

export default CaseDetailPage;
