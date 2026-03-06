import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Modal from '../utils/Modal';
import Button from '../utils/Button';
import './styles/PromptCard.css'

const PromptCard = ({ prompt, onDelete }) => {

  const navigate = useNavigate();
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  const handleEditClick = (e) => {
    e.stopPropagation();
    navigate(`/edit-prompt/${prompt.id}`);
  };

  const handleCardClick = () => {
    navigate(`/prompt/${prompt.id}`);
  };

  const confirmDelete = () => {
    onDelete(prompt.id);
    setShowDeleteModal(false);
  };

  return (
    <>
      <div className="prompt-card" onClick={handleCardClick}>
        <h2>{prompt.title}</h2>
        <p>{prompt.description}</p>

        <div className="prompt-card-buttons">

          <Button
            className="edit-button"
            onClick={handleEditClick}
          >
            Edit
          </Button>

          <Button
            className="delete-button"
            onClick={(e) => {
              e.stopPropagation();
              setShowDeleteModal(true);
            }}
          >
            Delete
          </Button>

        </div>
      </div>

      <Modal
        isVisible={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
      >
        <div className="delete-modal">

          <h3>Delete Prompt</h3>

          <p>
            Are you sure you want to delete
            <strong> "{prompt.title}"</strong>?
          </p>

          <div className="modal-actions">

            <Button
              className="cancel-button"
              onClick={() => setShowDeleteModal(false)}
            >
              Cancel
            </Button>

            <Button
              className="confirm-delete-button"
              onClick={confirmDelete}
            >
              Delete
            </Button>

          </div>

        </div>
      </Modal>
    </>
  );
};

export default PromptCard;