import React from "react";
import "./styles/ErrorMessage.css";

const ErrorMessage = ({ message }) => {

  return (
    <div className="error-container">

      <div className="error-card">

        <div className="error-icon">⚠</div>

        <h2>Something went wrong</h2>

        <p>{message}</p>

      </div>

    </div>
  );

};

export default ErrorMessage;