import React from "react";
import "./styles/SuccessCard.css";

const SuccessCard = ({ title, message }) => {
  return (
    <div className="success-card-container">
      <div className="success-card">

        <div className="success-icon">✓</div>

        <h2>{title}</h2>

        <p>{message}</p>

      </div>
    </div>
  );
};

export default SuccessCard;