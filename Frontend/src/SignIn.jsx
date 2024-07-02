// src/components/SignIn.jsx
import React from "react";
import { authentication } from "./components/Firebase/Firebase";
import { GoogleAuthProvider, signInWithPopup } from "firebase/auth";
import { useNavigate } from "react-router-dom";
import Button from "@mui/material/Button";

export default function SignIn() {
  const navigate = useNavigate();

  const signInWithGoogle = () => {
    const provider = new GoogleAuthProvider();
    // Adding the prompt parameter to force account selection
    provider.setCustomParameters({
      prompt: "select_account",
    });
    signInWithPopup(authentication, provider)
      .then((result) => {
        console.log(result);
        navigate("/homepage");
      })
      .catch((error) => {
        console.error("Error signing in with Google: ", error);
      });
  };

  return (
    <div>
      <h2>Sign In / Sign Up</h2>
      <Button variant="contained" onClick={signInWithGoogle}>
        Sign In / Sign Up with Google
      </Button>
    </div>
  );
}
