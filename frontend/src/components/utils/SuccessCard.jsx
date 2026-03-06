import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./styles/SuccessCard.css";

const SuccessCard = ({ title, message, redirectTo = "/" }) => {

  const navigate = useNavigate();

  useEffect(() => {

    const timer = setTimeout(() => {
      navigate(redirectTo);
    }, 2000);

    return () => clearTimeout(timer);

  }, [navigate, redirectTo]);

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