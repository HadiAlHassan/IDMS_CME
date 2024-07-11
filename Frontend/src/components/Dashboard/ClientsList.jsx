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
import classes from "./ClientsList.module.css";

function ClientListCard() {
  const [clients, setClients] = useState([]);

  useEffect(() => {
    const fetchClients = async () => {
      try {
        const response = await axios.post(
          "http://localhost:8000/api/user-clients",
          { user_id: localStorage["firebase_id"] } // Replace with actual user ID
        );
        console.log(response.data.clients);
        setClients(response.data.clients);
      } catch (error) {
        console.error("Error fetching clients:", error);
      }
    };
    fetchClients();
  }, []);

  return (
    <>
      <h2 className={classes.title}>Your Ongoing Clients</h2>
      <div className={classes.clientsContainer}>
        {clients.slice(0, 6).map((client, index) => (
          <Card key={index} className={classes.clientCard}>
            <CardContent className={classes.cardContent}>
              <Typography variant="h6" className={classes.clientName}>
                {client}
              </Typography>
            </CardContent>
          </Card>
        ))}
      </div>
    </>
  );
}

export default ClientListCard;
