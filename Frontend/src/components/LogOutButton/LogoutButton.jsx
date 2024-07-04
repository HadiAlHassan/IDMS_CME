// src/components/LogoutButton.jsx
import React from "react";
import { Button } from "@mui/material";
import { useAuth } from "../Context/AuthContext";
import { useNavigate } from "react-router-dom";
import classes from "./LogoutButton.module.css";
const LogoutButton = () => {
  const { logout } = useAuth();

  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/"); // Redirect to sign-in page after logout
  };

  return (
    <Button
      variant="contained"
      className={classes.logoutButton}
      onClick={handleLogout}
    >
      Log Out
    </Button>
  );
};

export default LogoutButton;
