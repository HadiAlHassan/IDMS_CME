import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../components/Context/AuthContext";

const PrivateRoute = ({ element: Element, ...rest }) => {
  const { currentUser, loading } = useAuth();

  console.log("PrivateRoute user:", currentUser);
  console.log("PrivateRoute loading:", loading);

  if (loading) {
    return <div>Loading...</div>; // Optional: Add a loading spinner or component here
  }

  if (!currentUser) {
    console.log("Not authenticated, redirecting to sign-in page.");
    return <Navigate to="/" />;
  }

  console.log("Authenticated, rendering the requested page.");
  return <Element {...rest} />;
};

export default PrivateRoute;
