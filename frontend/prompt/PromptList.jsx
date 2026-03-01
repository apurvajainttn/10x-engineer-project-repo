import React from 'react';
import PromptCard from './PromptCard';

const PromptList = ({ prompts }) => {
  return (
    <div className="prompt-list">
      {prompts.map(prompt => (
        <PromptCard key={prompt.id} prompt={prompt} />
      ))}
    </div>
  );
};

export default PromptList;
