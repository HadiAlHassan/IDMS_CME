// src/context/AuthContext.js
import React, { createContext, useContext, useEffect, useState } from "react";
import { useAuthState } from "react-firebase-hooks/auth";
import { auth } from "../Firebase/Firebase";

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [user, loading, error] = useAuthState(auth);
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    if (!loading) {
      setCurrentUser(user);
    }
  }, [user, loading]);

  const value = {
    currentUser,
    loading,
    error,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
