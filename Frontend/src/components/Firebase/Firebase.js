// src/components/Firebase/Firebase.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyBPDVCBr4qzEmEMuq9U_SWoCCXzBI4UmIc",
  authDomain: "idms-a1c57.firebaseapp.com",
  projectId: "idms-a1c57",
  storageBucket: "idms-a1c57.appspot.com",
  messagingSenderId: "287855361713",
  appId: "1:287855361713:web:771954928f92d21a976c90",
  measurementId: "G-3GSMZDVBS7",
};

const app = initializeApp(firebaseConfig);
export const authentication = getAuth(app);
