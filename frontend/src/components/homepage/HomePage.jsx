import React from 'react';
import Button from '../../components/utils/Button'
import './styles/HomePage.css';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {

  const navigate = useNavigate();

  const handleCreatePromptClick = () => {
    navigate(`/create-prompt`);
  };

  const handleListPromptsClick = () => {
    navigate(`/browse-prompts`);
  };

  return (
    <div className="home-container">
      <h1 className="home-title-first">Welcome to</h1>
      <h1 className="home-title-second">Prompt Lab!</h1>
      <h2 className="home-sub-title">Create, list and manage your prompts with ease</h2>
      <div className="button-group">
        <Button className="action-button" onClick={handleCreatePromptClick}>
          Create Prompt
        </Button>
        <Button className="action-button" onClick={handleListPromptsClick}>
          Browse Prompts
        </Button>
      </div>
    </div>
  );
};

export default HomePage;
