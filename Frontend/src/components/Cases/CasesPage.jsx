import React, { useState, useEffect } from "react";
import { Card, CardContent, Typography, Fab } from "@mui/material";
import { useNavigate } from "react-router-dom";
import classes from "./CasesPage.module.css";
import Header from "../Header/Header";
import AddCaseModal from "../Cases/AddCaseModal";
import AddIcon from "@mui/icons-material/Add";

const mockData = [
  {
    id: 1,
    caseName: "Case 1",
    clientName: "Client 1",
    caseStatus: "Open",
    openedDate: "2024-07-01T12:00:00Z",
    trialDates: ["2024-08-01", "2024-09-01"],
    documents: ["Document 1", "Document 2"],
  },
  {
    id: 2,
    caseName: "Case 2",
    clientName: "Client 2",
    caseStatus: "Closed",
    openedDate: "2024-06-01T12:00:00Z",
    trialDates: ["2024-07-01", "2024-08-01"],
    documents: [{ name: "Document 1", link: "http://example.com/doc1" }],
  },
  {
    id: 3,
    caseName: "Case 3",
    clientName: "Client 3",
    caseStatus: "Open",
    openedDate: "2024-08-01T12:00:00Z",
    trialDates: ["2024-09-01", "2024-012-01"],
    documents: [
      { name: "Document 1", link: "http://example.com/doc1" },
      { name: "Document 2", link: "http://example.com/doc2" },
    ],
  },
  {
    id: 4,
    caseName: "Case 4",
    clientName: "Client 4",
    caseStatus: "Closed",
    openedDate: "2024-03-01T12:00:00Z",
    trialDates: ["2024-12-01", "2024-11-01"],
    documents: [{ name: "Document 1", link: "http://example.com/doc1" }],
  },
  {
    id: 5,
    caseName: "Case 1",
    clientName: "Client 1",
    caseStatus: "Open",
    openedDate: "2024-07-01T12:00:00Z",
    trialDates: ["2024-08-01", "2024-09-01"],
    documents: [
      { name: "Document 1", link: "http://example.com/doc1" },
      { name: "Document 2", link: "http://example.com/doc2" },
    ],
  },
  {
    id: 6,
    caseName: "Case 2",
    clientName: "Client 2",
    caseStatus: "Closed",
    openedDate: "2024-06-01T12:00:00Z",
    trialDates: ["2024-07-01", "2024-08-01"],
    documents: [{ name: "Document 1", link: "http://example.com/doc1" }],
  },
  {
    id: 7,
    caseName: "Case 3",
    clientName: "Client 3",
    caseStatus: "Open",
    openedDate: "2024-08-01T12:00:00Z",
    trialDates: ["2024-09-01", "2024-012-01"],
    documents: [
      { name: "Document 1", link: "http://example.com/doc1" },
      { name: "Document 2", link: "http://example.com/doc2" },
    ],
  },
  {
    id: 8,
    caseName: "Case 4",
    clientName: "Client 4",
    caseStatus: "Closed",
    openedDate: "2024-03-01T12:00:00Z",
    trialDates: ["2024-12-01", "2024-11-01"],
    documents: [{ name: "Document 1", link: "http://example.com/doc1" }],
  },
];

const CasesPage = () => {
  const [cases, setCases] = useState([]);
  const [openAddCaseModal, setOpenAddCaseModal] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    setCases(mockData);
  }, []);

  const handleOpenAddCaseModal = () => {
    setOpenAddCaseModal(true);
  };

  const handleCloseAddCaseModal = () => {
    setOpenAddCaseModal(false);
  };

  const handleCaseClick = (id) => {
    navigate(`/cases/${id}`);
  };

  const getStatusClass = (status) => {
    if (status === "Open") return classes.openStatus;
    if (status === "Closed") return classes.closedStatus;
    if (status === "Pending") return classes.pendingStatus;
  };

  return (
    <>
      <Header />
      <div className={classes.casesContainer}>
        {cases.map((caseItem) => (
          <Card
            key={caseItem.id}
            className={classes.caseCard}
            onClick={() => handleCaseClick(caseItem.id)}
          >
            <CardContent>
              <Typography variant="h5" className={classes.caseTitle}>
                {caseItem.caseName}
              </Typography>
              <Typography className={classes.caseDetail}>
                Client: {caseItem.clientName}
              </Typography>
              <Typography
                className={`${classes.caseDetail} ${getStatusClass(
                  caseItem.caseStatus
                )}`}
              >
                Status: {caseItem.caseStatus}
              </Typography>
            </CardContent>
          </Card>
        ))}
      </div>
      <Fab
        color="primary"
        aria-label="add"
        className={classes.fab}
        onClick={handleOpenAddCaseModal}
      >
        <AddIcon />
      </Fab>
      <AddCaseModal open={openAddCaseModal} onClose={handleCloseAddCaseModal} />
    </>
  );
};

export default CasesPage;
