import React from 'react';
import './styles/CollectionCard.css';
import Button from '../utils/Button';

const CollectionCard = ({ collection, onDelete }) => {

  const handleDeleteClick = (e) => {
    e.stopPropagation();

    const confirmDelete = window.confirm(
      `Are you sure you want to delete the collection: "${collection.name}"?`
    );

    if (confirmDelete) {
      onDelete(collection.id);
    }
  };

  return (
    <div className="collection-card">

      <h3>{collection.name}</h3>

      <p>{collection.description}</p>

      <div className="collection-card-buttons">
        <Button onClick={handleDeleteClick} className="delete-button">
          Delete
        </Button>
      </div>

    </div>
  );
};

export default CollectionCard;