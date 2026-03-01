import React, { useState } from 'react';

const CollectionForm = ({ onSubmit }) => {
  const [name, setName] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ name });
  };

  return (
    <form onSubmit={handleSubmit} className="collection-form">
      <div>
        <label htmlFor="collection-name">Collection Name</label>
        <input
          type="text"
          id="collection-name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </div>
      <button type="submit">Create Collection</button>
    </form>
  );
};

export default CollectionForm;
