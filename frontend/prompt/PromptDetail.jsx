import React from 'react';

const PromptDetail = ({ prompt }) => {
  return (
    <div className="prompt-detail">
      <h1>{prompt.title}</h1>
      <p>{prompt.description}</p>
      {/* Add more detailed information about the prompt here */}
    </div>
  );
};

export default PromptDetail;
