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

  const handleViewClick = (e) => {
    e.stopPropagation();
    navigate(`/prompt/${prompt.id}`);
  };

  const confirmDelete = () => {
    onDelete(prompt.id);
    setShowDeleteModal(false);
  };

  return (
    <>
      <div className="prompt-card">

        <h2>{prompt.title}</h2>
        <p>{prompt.description}</p>

        {/* Primary action */}
        <Button
          className="view-details-button"
          onClick={handleViewClick}
        >
          View Details
        </Button>

        {/* Secondary actions */}
        <div className="prompt-card-secondary-actions">

          <button
            className="icon-button edit-icon-button"
            onClick={handleEditClick}
            data-tooltip="Edit"
          >
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 20h9" />
              <path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5z" />
            </svg>
          </button>

          <button
            className="icon-button delete-icon-button"
            onClick={(e) => {
              e.stopPropagation();
              setShowDeleteModal(true);
            }}
            data-tooltip="Delete"
          >
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="3 6 5 6 21 6" />
              <path d="M19 6l-1 14H6L5 6" />
              <path d="M10 11v6" />
              <path d="M14 11v6" />
              <path d="M9 6V4h6v2" />
            </svg>
          </button>

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