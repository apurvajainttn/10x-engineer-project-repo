// frontend/src/components/collection/CollectionCard.jsx
import React from 'react';

const CollectionCard = ({ collection, onDelete }) => {
  const handleDeleteClick = () => {
    const confirmDelete = window.confirm(`Are you sure you want to delete the collection: "${collection.name}"?`);
    if (confirmDelete) {
      onDelete(collection.id);
    }
  };

  return (
    <div className="collection-card">
      <h3>{collection.name}</h3>
      <p>{collection.description}</p>
      <button onClick={handleDeleteClick}>Delete</button>
    </div>
  );
};

export default CollectionCard;