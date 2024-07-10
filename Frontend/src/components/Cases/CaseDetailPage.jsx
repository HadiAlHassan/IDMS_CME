import React, { useState } from "react";
import { useParams } from "react-router-dom";
import { Card, CardContent, Typography, Button } from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import classes from "./CaseDetailPage.module.css";
import Header from "../Header/Header";
import EditCaseModal from "../Cases/EditCaseModal";

const mockData = [
  {
    id: 1,
    caseName: "Case 1",
    clientName: "Client 1",
    caseStatus: "Open",
    openedDate: "2024-07-01T12:00:00Z",
    trialDates: ["2024-08-01", "2024-09-01"],
    documents: ["Doc1", "Doc2"],
  },
  {
    id: 2,
    caseName: "Case 2",
    clientName: "Client 2",
    caseStatus: "Closed",
    openedDate: "2024-06-01T12:00:00Z",
    trialDates: ["2024-07-01", "2024-08-01"],
    documents: ["Doc1", "Doc2"],
  },
  // Add more mock data as needed
];

const CaseDetailPage = () => {
  const { id } = useParams();
  const caseItem = mockData.find((caseItem) => caseItem.id === parseInt(id));
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [updatedCase, setUpdatedCase] = useState(caseItem);

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
              {updatedCase.caseName}
            </Typography>
            <Typography className={classes.caseDetail}>
              Client: {updatedCase.clientName}
            </Typography>
            <Typography
              className={`${classes.caseDetail} ${getStatusClass(
                updatedCase.caseStatus
              )}`}
            >
              Status: {updatedCase.caseStatus}
            </Typography>
            <Typography className={classes.caseDetail}>
              Opened: {new Date(updatedCase.openedDate).toLocaleString()}
            </Typography>
            <Typography className={classes.caseDetail}>
              Important Dates: {updatedCase.trialDates.join(", ")}
            </Typography>
            <Typography className={classes.caseDetail}>
              Related Documents:
              <ul>
                {updatedCase.documents.map((doc, index) => (
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
