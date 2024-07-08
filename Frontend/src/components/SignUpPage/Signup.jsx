import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, TextField } from "@mui/material";
import axios from "axios";
import classes from "./SignUp.module.css";

export default function SignUp() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleKeyPress = (event) => {
    if (event.key === "Enter") {
      signUp();
    }
  };

  const signUp = async () => {
    try {
      const response = await axios.post("http://localhost:8000/api/signup", {
        email,
        password,
        first_name: firstName,
        last_name: lastName,
      });
      const userData = response.data.user;
      localStorage.setItem("token", userData["idToken"]);

      console.log("Successfully signed up:", userData);

      navigate("/homepage"); // Navigate to homepage on successful sign-up
    } catch (err) {
      setError(err.response?.data?.message || "An error occurred");
    }
  };

  return (
    <div className={classes.signUpContainer}>
      <div className={classes.card}>
        <h2>Create an Account</h2>
        <p>Sign up to get started</p>
        <TextField
          label="First Name"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          fullWidth
          margin="normal"
          onKeyDown={handleKeyPress}
        />
        <TextField
          label="Last Name"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
          fullWidth
          margin="normal"
          onKeyDown={handleKeyPress}
        />
        <TextField
          label="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          fullWidth
          margin="normal"
          onKeyDown={handleKeyPress}
        />
        <TextField
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          fullWidth
          margin="normal"
          onKeyDown={handleKeyPress}
        />
        {error && <p className={classes.error}>{error}</p>}
        <Button
          variant="contained"
          className={classes.signUpButton}
          onClick={signUp}
        >
          Sign Up
        </Button>
      </div>
    </div>
  );
}
