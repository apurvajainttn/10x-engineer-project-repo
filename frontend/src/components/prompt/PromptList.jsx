import React, { useState, useEffect } from 'react';
import { getPrompts, deletePrompt } from '../../api/prompts';
import { getCollections } from '../../api/collections'; // Import collections API
import PromptCard from './PromptCard';
import LoadingSpinner from '../utils/LoadingSpinner';
import ErrorMessage from '../utils/ErrorMessage';
import './styles/PromptList.css'
import SearchBar from '../utils/SearchBar';

const PromptList = () => {
  const [prompts, setPrompts] = useState([]);
  const [collections, setCollections] = useState([]);
  const [selectedCollection, setSelectedCollection] = useState('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [promptsData, collectionsData] = await Promise.all([
          getPrompts(),
          getCollections(),
        ]);
        setPrompts(promptsData.prompts);
        setCollections(collectionsData.collections);
        setLoading(false);
      } catch (err) {
        setError(err);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleDelete = async (id) => {
    try {
      const response = await deletePrompt(id);
      console.log("Response Code: ", response.status);
      if (response.status === 204) {
        setPrompts(prompts.filter(prompt => prompt.id !== id));
        setSuccessMessage('Prompt has been deleted successfully.');
        setTimeout(() => {
          setSuccessMessage('');
          if (prompts.length === 0) {
            setError({ message: 'No prompts found.' });
          }
        }, 3000);
      } else {
        throw new Error('Failed to delete the prompt');
      }
    } catch (err) {
      console.log("Error: ", err);
      setError(err);
    }
  };

  const handleCollectionChange = (e) => {
    setSelectedCollection(e.target.value);
  };

  const filteredPrompts = prompts.filter((prompt) => {

    const matchesCollection =
      selectedCollection === 'all' ||
      (selectedCollection === 'none' && !prompt.collection_id) ||
      prompt.collection_id === selectedCollection;

    const matchesSearch =
      prompt.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      prompt.description?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      prompt.content?.toLowerCase().includes(searchQuery.toLowerCase());

    return matchesCollection && matchesSearch;

  });

  if (loading) return <LoadingSpinner />;
  if (error && !successMessage) return <ErrorMessage message={error.message} />;

  return (
    <div className="prompt-list">
      <div className="page-header">
        <h1>Prompt Dashboard</h1>
        <p>Manage and organize your AI prompts</p>
      </div>
      {successMessage && <div className="success-message">{successMessage}</div>}

      <div className="toolbar">

        <SearchBar
          value={searchQuery}
          onChange={setSearchQuery}
          placeholder="Search prompts..."
        />

        <div className="collection-filter">
          <label htmlFor="collectionSelect">Filter by Collection:</label>
          <select
            id="collectionSelect"
            value={selectedCollection}
            onChange={handleCollectionChange}
          >
            <option value="all">All Collections</option>
            <option value="none">No Collection</option>

            {collections.map((collection) => (
              <option key={collection.id} value={collection.id}>
                {collection.name}
              </option>
            ))}
          </select>
        </div>

      </div>

      {filteredPrompts.length === 0 && !successMessage ? (
        <div className="no-prompts-message">No prompts found.</div>
      ) : (
        <div className="prompt-grid">
          {filteredPrompts.map((prompt) => (
            <PromptCard
              key={prompt.id}
              prompt={prompt}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default PromptList;