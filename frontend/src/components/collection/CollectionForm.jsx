import React, { useState } from 'react';
import { createCollection } from '../../api/collections'; // Import the API function for creating collection
import './styles/CollectionForm.css'
import Button from '../utils/Button';

const CollectionForm = () => {
  // State for form fields, success, and error handling
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await createCollection({ name, description });
      setSuccessMessage(`Collection "${name}" has been created successfully!`);
      setName('');
      setDescription('');
      setError(null);
    } catch (err) {
      console.error("Error:", err);
      setError('Failed to create collection. Please try again.');
      setSuccessMessage('');
    }
  };

  if (successMessage) {
    return (
      <div className="success-message">
        {successMessage}
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="collection-form">
      {error && <div className="error-message">{error}</div>}
      <div>
        <label htmlFor="collection-name">Collection Name</label>
        <input
          type="text"
          id="collection-name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          minLength={1}
          maxLength={100}
        />
      </div>
      <div>
        <label htmlFor="collection-description">Description</label>
        <textarea
          id="collection-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          maxLength={500}
        />
      </div>
      <Button type="submit">Create Collection</Button>
    </form>
  );
};

export default CollectionForm;