import React from 'react';

const PromptCard = ({ prompt }) => {
  return (
    <div className="prompt-card">
      <h2>{prompt.title}</h2>
      <p>{prompt.description}</p>
      {/* Add more prompt details here */}
    </div>
  );
};

export default PromptCard;
