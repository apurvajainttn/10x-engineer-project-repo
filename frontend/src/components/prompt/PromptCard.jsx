import React from 'react';
import { useNavigate } from 'react-router-dom';

const PromptCard = ({ prompt, onDelete }) => {
  const navigate = useNavigate(); 

  const handleDeleteClick = (e) => {
    e.stopPropagation(); // Prevent card click from triggering on delete
    const confirmDelete = window.confirm(`Are you sure you want to delete the prompt: "${prompt.title}"?`);
    if (confirmDelete) {
      onDelete(prompt.id);
    }
  };

  const handleEditClick = (e) => {
    e.stopPropagation(); // Prevent card click from triggering on edit
    navigate(`/edit-prompt/${prompt.id}`);
  };

  const handleCardClick = () => {
    navigate(`/prompt/${prompt.id}`);
  };

  return (
    <div className="prompt-card" onClick={handleCardClick}>
      <h2>{prompt.title}</h2>
      <p>{prompt.description}</p>
      <button onClick={handleEditClick} className="edit-button">Edit</button>
      <button onClick={handleDeleteClick} className="delete-button">Delete</button>
    </div>
  );
};

export default PromptCard;