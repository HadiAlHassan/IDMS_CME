import React, { createContext, useState } from "react";

export const UpdateContext = createContext();

export const UpdateProvider = ({ children }) => {
  const [updateWordCloud, setUpdateWordCloud] = useState(false);
  const [updatePieChart, setUpdatePieChart] = useState(false);

  const handleFileUploadSuccess = () => {
    setUpdateWordCloud((prev) => !prev); // Toggle the state to force re-render
    setUpdatePieChart((prev) => !prev);
  };

  return (
    <UpdateContext.Provider
      value={{ updateWordCloud, updatePieChart, handleFileUploadSuccess }}
    >
      {children}
    </UpdateContext.Provider>
  );
};
