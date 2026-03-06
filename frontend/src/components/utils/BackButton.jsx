import React from "react";
import { useNavigate } from "react-router-dom";
import "./styles/BackButton.css";

const BackButton = ({ label = "Back" }) => {

  const navigate = useNavigate();

  return (
    <button
      className="back-button"
      onClick={() => navigate(-1)}
    >
      ← {label}
    </button>
  );
};

export default BackButton;