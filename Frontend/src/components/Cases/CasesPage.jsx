import React, { useState, useEffect } from "react";
import { Card, CardContent, Typography, Fab } from "@mui/material";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import classes from "./CasesPage.module.css";
import Header from "../Header/Header";
import AddCaseModal from "../Cases/AddCaseModal";
import AddIcon from "@mui/icons-material/Add";

const CasesPage = () => {
  const [cases, setCases] = useState([]);
  const [openAddCaseModal, setOpenAddCaseModal] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCases = async () => {
      try {
        const userId = localStorage.getItem("firebase_id"); // Retrieve user ID from localStorage
        const response = await axios.post(
          "http://localhost:8000/api/get-cases-by-user",
          {
            user_id: userId,
          }
        );
        setCases(response.data.cases);
      } catch (error) {
        console.error("Error fetching cases:", error);
      }
    };

    fetchCases();
  }, []);

  const handleOpenAddCaseModal = () => {
    setOpenAddCaseModal(true);
  };

  const handleCloseAddCaseModal = () => {
    setOpenAddCaseModal(false);
  };

  const handleCaseClick = (name) => {
    navigate(`/cases/${name}`);
  };

  const getStatusClass = (status) => {
    if (status === "Open") return classes.openStatus;
    if (status === "Closed") return classes.closedStatus;
    if (status === "Pending") return classes.pendingStatus;
  };

  const addCase = (newCase) => {
    setCases([...cases, newCase]);
  };

  return (
    <>
      <Header />
      <div className={classes.casesContainer}>
        {cases.length === 0 ? (
          <Typography variant="h6" className={classes.noCasesMessage}>
            You currently have no ongoing cases
          </Typography>
        ) : (
          cases.map((caseItem) => (
            <Card
              key={caseItem.name}
              className={classes.caseCard}
              onClick={() => handleCaseClick(caseItem.name)}
            >
              <CardContent>
                <Typography variant="h5" className={classes.caseTitle}>
                  {caseItem.name}
                </Typography>
                <Typography className={classes.caseDetail}>
                  Client: {caseItem.client}
                </Typography>
                <Typography
                  className={`${classes.caseDetail} ${getStatusClass(
                    caseItem.status
                  )}`}
                >
                  Status: {caseItem.status}
                </Typography>
              </CardContent>
            </Card>
          ))
        )}
      </div>
      <Fab
        color="primary"
        aria-label="add"
        className={classes.fab}
        onClick={handleOpenAddCaseModal}
      >
        <AddIcon />
      </Fab>
      <AddCaseModal
        open={openAddCaseModal}
        onClose={handleCloseAddCaseModal}
        addCase={addCase}
      />
    </>
  );
};

export default CasesPage;
