import React, { useEffect } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../components/Context/AuthContext";

const PrivateRoute = ({ element: Element, ...rest }) => {
  const { currentUser } = useAuth();
  console.log(
    "private route",
    currentUser || localStorage.getItem("token") != null
  );

  if (currentUser || localStorage.getItem("token") != null) {
    return <Element {...rest} />;
  }
  return <Navigate to="/" />;
};

export default PrivateRoute;
