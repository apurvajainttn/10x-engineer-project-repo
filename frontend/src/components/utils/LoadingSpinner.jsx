import React from 'react';
import './styles/LoadingSpinner.css';

const LoadingSpinner = () => {
  return (
    <div className="loading-container">

      <div className="gradient-spinner"></div>

      <p className="loading-text">Loading...</p>

    </div>
  );
};

export default LoadingSpinner;