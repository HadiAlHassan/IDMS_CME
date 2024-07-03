// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBPDVCBr4qzEmEMuq9U_SWoCCXzBI4UmIc",
  authDomain: "idms-a1c57.firebaseapp.com",
  projectId: "idms-a1c57",
  storageBucket: "idms-a1c57.appspot.com",
  messagingSenderId: "287855361713",
  appId: "1:287855361713:web:771954928f92d21a976c90",
  measurementId: "G-3GSMZDVBS7",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export { auth, app };
