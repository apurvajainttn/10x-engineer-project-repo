import React, { useState, useEffect } from 'react';
import { createPrompt, updatePrompt } from '../../api/prompts';
import { getCollections } from '../../api/collections';

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
    if (formData.title.length < 1 || formData.title.length > 200) {
      alert('Title must be between 1 and 200 characters');
      return;
    }
    if (formData.content.length < 1) {
      alert('Content must not be empty');
      return;
    }

    console.log('Apurva_Test Submitting form data:', formData);

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
      console.error("Error:", err);
      setError('Failed to process prompt. Please try again.');
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
    <form onSubmit={handleSubmit} className="prompt-form">
      {error && <div className="error-message">{error}</div>}
      <div>
        <label htmlFor="title">Title</label>
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
      <div>
        <label htmlFor="content">Content</label>
        <textarea
          id="content"
          name="content"
          value={formData.content}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          maxLength={500}
        />
      </div>
      <div>
        <label htmlFor="tags">Tags (comma-separated)</label>
        <input
          type="text"
          id="tags"
          name="tags"
          value={formData.tags.join(', ')}
          onChange={handleTagsChange}
        />
      </div>
      <div>
        <label htmlFor="collection">Collection (optional)</label>
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
      <button type="submit">{isEditing ? 'Update' : 'Create'} Prompt</button>
    </form>
  );
};

export default PromptForm;