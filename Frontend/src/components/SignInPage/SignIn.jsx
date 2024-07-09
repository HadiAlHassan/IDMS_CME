import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, TextField } from "@mui/material";
import axios from "axios";
import classes from "./SignIn.module.css";

export default function SignIn() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const signIn = async () => {
    try {
      const response = await axios.post("http://localhost:8000/api/login", {
        email,
        password,
      });
      const userData = response.data.user;
      localStorage.setItem("token", userData["idToken"]);
      localStorage.setItem("email", userData["email"]);
      console.log("Successfully logged in:", userData);
      navigate("/homepage"); // Navigate to homepage on successful login
    } catch (err) {
      setError(err.response?.data?.message || "An error occurred");
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === "Enter") {
      signIn();
    }
  };

  const navigateToSignUp = () => {
    navigate("/signup");
  };

  return (
    <div className={classes.signInContainer}>
      <div className={classes.card}>
        <h2>Welcome to IDMS</h2>
        <p>Sign in to continue</p>
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
          className={classes.googleButton}
          onClick={signIn}
        >
          Sign In
        </Button>
        <hr className={classes.separator} />
        <div className={classes.signUpContainer}>
          <p>Not a user?</p>
          <Button
            variant="outlined"
            className={classes.signUpButton}
            onClick={navigateToSignUp}
          >
            Sign Up
          </Button>
        </div>
      </div>
    </div>
  );
}
