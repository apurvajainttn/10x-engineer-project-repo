import React, { useState } from 'react';
import './styles/CollectionCard.css';
import Button from '../utils/Button';
import Modal from '../utils/Modal';

const CollectionCard = ({ collection, onDelete }) => {

  const [showDeleteModal, setShowDeleteModal] = useState(false);

  const confirmDelete = () => {
    onDelete(collection.id);
    setShowDeleteModal(false);
  };

  return (
    <>
      <div className="collection-card">

        <h3>{collection.name}</h3>

        <p>{collection.description}</p>

        <div className="collection-card-buttons">
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

          <h3>Delete Collection</h3>

          <p>
            Are you sure you want to delete
            <strong> "{collection.name}"</strong>?
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

export default CollectionCard;