import React, { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";
import axios from "axios";
import classes from "./UpcomingTrialsCard.module.css";
function UpcomingTrialsCard() {
  const [trials, setTrials] = useState([]);

  useEffect(() => {
    const fetchTrials = async () => {
      try {
        const response = await axios.post(
          "http://localhost:8000/api/upcoming-trials",
          { user_id: localStorage["firebase_id"] } // Replace with actual user ID
        );
        setTrials(response.data.upcoming_trials);
      } catch (error) {
        console.error("Error fetching trial dates:", error);
      }
    };
    fetchTrials();
  }, []);

  const getDateColor = (date) => {
    const today = new Date();
    const trialDate = new Date(date);
    const timeDiff = trialDate.getTime() - today.getTime();
    const dayDiff = timeDiff / (1000 * 3600 * 24);

    if (dayDiff <= 7) {
      return "red";
    } else if (dayDiff <= 30) {
      return "gold";
    } else {
      return "green";
    }
  };

  return (
    <>
      <h2 className={classes.title}>Your Upcoming Trials</h2>
      <div className={classes.upcomingTrialsContainer}>
        <List
          sx={{
            display: "flex",
            flexDirection: "row",
            flexWrap: "wrap",
            justifyContent: "center",
            gap: 2,
          }}
        >
          {trials.slice(0, 6).map((trial) => (
            <ListItem
              key={trial.caseId}
              sx={{
                backgroundColor: "#ffffff",
                borderRadius: 2,
                boxShadow: 1,
                padding: 2,
                textAlign: "center",
                width: 200,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <ListItemText
                primary={trial.caseName}
                secondary={`Date: ${trial.date}`}
                primaryTypographyProps={{
                  sx: { fontWeight: "bold", color: "black" },
                }}
                secondaryTypographyProps={{
                  sx: { color: getDateColor(trial.date) },
                }}
              />
            </ListItem>
          ))}
        </List>
      </div>
    </>
  );
}

export default UpcomingTrialsCard;
