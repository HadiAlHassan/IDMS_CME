// src/components/PrivateRoute.jsx
import React from "react";
import { Route, Navigate } from "react-router-dom";
import { useAuthState } from "react-firebase-hooks/auth";
import { authentication } from "../components/Firebase/Firebase";

const PrivateRoute = ({ element: Element, ...rest }) => {
  const [user, loading] = useAuthState(authentication);

  if (loading) {
    return <div>Loading...</div>;
  }

  return user ? <Element {...rest} /> : <Navigate to="/" />;
};

export default PrivateRoute;
