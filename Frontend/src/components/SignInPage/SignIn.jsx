import React from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@mui/material";
import { signInWithPopup, GoogleAuthProvider } from "firebase/auth";
import { auth } from "../Firebase/Firebase";
import classes from "./SignIn.module.css";

export default function SignIn() {
  const navigate = useNavigate();

  const signInWithGoogle = () => {
    const provider = new GoogleAuthProvider();
    provider.setCustomParameters({
      prompt: "select_account",
    });
    signInWithPopup(auth, provider)
      .then((result) => {
        console.log(result);
        navigate("/homepage");
      })
      .catch((error) => {
        console.error("Error signing in with Google: ", error);
      });
  };

  return (
    <div className={classes.signInContainer}>
      <div className={classes.card}>
        <h2>Welcome to IDMS</h2>
        <p>Sign in to continue</p>
        <Button
          variant="contained"
          className={classes.googleButton}
          onClick={signInWithGoogle}
        >
          Sign In with Google
        </Button>
      </div>
    </div>
  );
}
