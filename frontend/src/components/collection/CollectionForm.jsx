import React, { useState } from 'react';
import { createCollection } from '../../api/collections';
import './styles/CollectionForm.css';
import Button from '../utils/Button';
import SuccessCard from '../utils/SuccessCard';
import BackButton from '../utils/BackButton';

const CollectionForm = () => {

  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await createCollection({ name, description });

      setSuccessMessage(`Collection "${name}" has been created successfully!`);

      setName('');
      setDescription('');
      setError(null);

    } catch (err) {
      console.error(err);
      setError('Failed to create collection. Please try again.');
      setSuccessMessage('');
    }
  };

  if (successMessage) {
    return (
      <SuccessCard
        title="Collection Created"
        message={successMessage}
      />
    );
  }

  return (
    <div className="collection-form-page">

      <div className="collection-form-header">
        <BackButton />

        <div className="collection-form-header-text">
          <h1>Create Collection</h1>
          <p>Organize your prompts into collections</p>
        </div>

      </div>

      <form onSubmit={handleSubmit} className="collection-form">

        {error && <div className="error-message">{error}</div>}

        <div className="form-group">
          <label htmlFor="collection-name">
            Collection Name <span className="required">*</span>
          </label>

          <input
            type="text"
            id="collection-name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            maxLength={100}
          />
        </div>

        <div className="form-group">
          <label htmlFor="collection-description">
            Description <span className="required">*</span>
          </label>

          <textarea
            id="collection-description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
            maxLength={500}
          />
        </div>

        <Button className="submit-button" type="submit">Create Collection</Button>

      </form>

    </div>
  );
};

export default CollectionForm;