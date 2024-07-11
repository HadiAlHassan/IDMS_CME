import React, { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Box,
} from "@mui/material";
import axios from "axios";
import classes from "./UserCaseCount.module.css";

function UserCaseCountsCard() {
  const [caseCounts, setCaseCounts] = useState({
    Open: 0,
    Closed: 0,
    Pending: 0,
  });

  useEffect(() => {
    const fetchCaseCounts = async () => {
      try {
        const response = await axios.post(
          "http://localhost:8000/api/user-case-counts",
          { user_id: localStorage["firebase_id"] } // Replace with actual user ID
        );
        setCaseCounts(response.data);
      } catch (error) {
        console.error("Error fetching case counts:", error);
      }
    };
    fetchCaseCounts();
  }, []);

  return (
    <>
      <h2 className={classes.title}>Your Cases Status</h2>
      <Card className={classes.card}>
        <CardContent className={classes.cardContent}>
          <Box className={classes.circlesContainer}>
            <Box className={classes.circleItem}>
              <Typography variant="h6" className={classes.circleLabel}>
                Open
              </Typography>
              <Box className={classes.circle} sx={{ backgroundColor: "green" }}>
                <Typography variant="subtitle1" className={classes.circleValue}>
                  {caseCounts.Open}
                </Typography>
              </Box>
            </Box>
            <Box className={classes.circleItem}>
              <Typography variant="h6" className={classes.circleLabel}>
                Pending
              </Typography>
              <Box className={classes.circle} sx={{ backgroundColor: "gold" }}>
                <Typography variant="subtitle1" className={classes.circleValue}>
                  {caseCounts.Pending}
                </Typography>
              </Box>
            </Box>
            <Box className={classes.circleItem}>
              <Typography variant="h6" className={classes.circleLabel}>
                Closed
              </Typography>
              <Box className={classes.circle} sx={{ backgroundColor: "red" }}>
                <Typography variant="subtitle1" className={classes.circleValue}>
                  {caseCounts.Closed}
                </Typography>
              </Box>
            </Box>
          </Box>
        </CardContent>
      </Card>
    </>
  );
}

export default UserCaseCountsCard;
