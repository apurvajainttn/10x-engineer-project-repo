import React, { useState, useEffect } from 'react';
import { createPrompt, updatePrompt } from '../../api/prompts';
import { getCollections } from '../../api/collections';
import './styles/PromptForm.css'
import Button from '../utils/Button';
import SuccessCard from '../utils/SuccessCard';
import BackButton from '../utils/BackButton';

const PromptForm = ({ initialData = {}, isEditing = false }) => {
  const [formData, setFormData] = useState({
    title: initialData.title || '',
    content: initialData.content || '',
    description: initialData.description || '',
    tags: initialData.tags || [],
    collection_id: initialData.collection_id || '',  // Adding collection_id
  });
  const [collections, setCollections] = useState([]);  // Ensure collections is always an array
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    // Fetching collections when component mounts
    const fetchCollections = async () => {
      try {
        const responseData = await getCollections();
        if (responseData && Array.isArray(responseData.collections)) {
          setCollections(responseData.collections);
        } else {
          console.error("Fetched collections data is not valid:", responseData);
          setCollections([]);  // Set to an empty array if not valid
        }
      } catch (err) {
        console.error("Failed to fetch collections:", err);
        setCollections([]);  // Set to an empty array on fetch error
      }
    };
    fetchCollections();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleTagsChange = (e) => {
    const { value } = e.target;
    setFormData({
      ...formData,
      tags: value.split(',').map(tag => tag.trim()),
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.title.length > 200) {
      setError("Title must be less than 200 characters.");
      return;
    }

    try {
      if (isEditing) {
        await updatePrompt(initialData.id, formData);
        setSuccessMessage(`Prompt "${formData.title}" has been updated successfully!`);
      } else {
        await createPrompt(formData);
        setSuccessMessage(`Prompt "${formData.title}" has been created successfully!`);
      }

      setError(null);

    } catch (err) {
      console.log("Error in submitting form", err)
      setError("Failed to process prompt. Please try again.");
      setSuccessMessage('');
    }
  };

  if (successMessage) {
    return (
      <SuccessCard
        title={isEditing ? "Prompt Updated" : "Prompt Created"}
        message={successMessage}
      />
    );
  }

  return (
    <div className="prompt-form-page">

      <div className="prompt-form-header">
        <BackButton />

        <div className="prompt-form-header-text">
          <h1>{isEditing ? "Edit Prompt" : "Create New Prompt"}</h1>
          <p>Create reusable prompts for your AI workflows</p>
        </div>

      </div>

      <form onSubmit={handleSubmit} className="prompt-form">

        <div className="form-section-header">
          <h3>Prompt Details</h3>
        </div>

        <p className="required-note">Fields marked with * are required</p>

        {error && <div className="error-message">{error}</div>}

        <div className="form-group">
          <label htmlFor="title">
            Title <span className="required">*</span>
          </label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            minLength={1}
            maxLength={200}
          />
        </div>

        <div className="form-group">
          <label htmlFor="content">
            Content <span className="required">*</span>
          </label>
          <textarea
            id="content"
            name="content"
            value={formData.content}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">
            Description <span className="required">*</span>
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
            maxLength={500}
          />
        </div>

        <div className="form-group">
          <label htmlFor="tags">Tags</label>
          <input
            type="text"
            id="tags"
            name="tags"
            value={formData.tags.join(', ')}
            onChange={handleTagsChange}
            placeholder="ai, marketing, coding"
          />
        </div>

        <div className="form-group">
          <label htmlFor="collection">Collection</label>
          <select
            id="collection"
            name="collection_id"
            value={formData.collection_id}
            onChange={handleChange}
          >
            <option value="">No Collection</option>
            {collections.map(collection => (
              <option key={collection.id} value={collection.id}>
                {collection.name}
              </option>
            ))}
          </select>
        </div>

        <Button className="submit-button" type="submit">
          {isEditing ? "Update Prompt" : "Create Prompt"}
        </Button>

      </form>
    </div>
  );
};

export default PromptForm;