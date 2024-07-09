import React, { useState, useEffect } from "react";
import { Box, Card, CardContent, Typography, Grid, Fab } from "@mui/material";
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
    documents: [
      { name: "Document 1", link: "http://example.com/doc1" },
      { name: "Document 2", link: "http://example.com/doc2" },
    ],
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
  useEffect(() => {
    // Simulating an API call with mock data
    setCases(mockData);
  }, []);
  const handleOpenAddCaseModal = () => {
    setOpenAddCaseModal(true);
  };

  const handleCloseAddCaseModal = () => {
    setOpenAddCaseModal(false);
  };

  return (
    <>
      <Header />
      <div className={classes.casesContainer}>
        {cases.map((caseItem) => (
          <Card key={caseItem.id} className={classes.caseCard}>
            <CardContent>
              <Typography variant="h5" className={classes.caseTitle}>
                {caseItem.caseName}
              </Typography>
              <Typography className={classes.caseDetail}>
                Client: {caseItem.clientName}
              </Typography>
              <Typography className={classes.caseDetail}>
                Status: {caseItem.caseStatus}
              </Typography>
              <Typography className={classes.caseDetail}>
                Opened: {new Date(caseItem.openedDate).toLocaleString()}
              </Typography>
              <Typography className={classes.caseDetail}>
                Important Dates: {caseItem.trialDates.join(", ")}
              </Typography>
              <Typography className={classes.caseDetail}>
                Related Documents:
                <ul>
                  {caseItem.documents.map((doc, index) => (
                    <li key={index}>
                      <a
                        href={doc.link}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        {doc.name}
                      </a>
                    </li>
                  ))}
                </ul>
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
