import React, { createContext, useState } from "react";

export const UpdateContext = createContext();

export const UpdateProvider = ({ children }) => {
  const [updateWordCloud, setUpdateWordCloud] = useState(false);

  const handleFileUploadSuccess = () => {
    setUpdateWordCloud((prev) => !prev); // Toggle the state to force re-render
  };

  return (
    <UpdateContext.Provider
      value={{ updateWordCloud, handleFileUploadSuccess }}
    >
      {children}
    </UpdateContext.Provider>
  );
};
