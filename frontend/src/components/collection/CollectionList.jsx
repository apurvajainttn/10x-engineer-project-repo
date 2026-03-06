import React, { useState, useEffect } from 'react';
import { getCollections, deleteCollection } from '../../api/collections';
import CollectionCard from './CollectionCard';
import LoadingSpinner from '../utils/LoadingSpinner';
import ErrorMessage from '../utils/ErrorMessage';
import './styles/CollectionList.css';
import SearchBar from '../utils/SearchBar';

const CollectionList = () => {
  const [collections, setCollections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const fetchCollections = async () => {
      try {
        const data = await getCollections();
        setCollections(data.collections);
        setLoading(false);
      } catch (err) {
        setError(err);
        setLoading(false);
      }
    };
    fetchCollections();
  }, []);

  const handleDelete = async (id) => {
    try {
      const response = await deleteCollection(id);

      if (response.status === 204) {
        setCollections(collections.filter(collection => collection.id !== id));
        setSuccessMessage('Collection has been deleted successfully.');

        setTimeout(() => {
          setSuccessMessage('');
        }, 3000);

      } else {
        throw new Error('Failed to delete the collection');
      }
    } catch (err) {
      setError(err);
    }
  };

  const filteredCollections = collections.filter((collection) => {

    return (
      collection.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      collection.description?.toLowerCase().includes(searchQuery.toLowerCase())
    );

  });

  if (loading) return <LoadingSpinner />;
  if (error && !successMessage) return <ErrorMessage message={error.message} />;

  return (
    <div className="collection-list">

      <div className="page-header">
        <h1>Collections</h1>
        <p>Group prompts into collections</p>
      </div>

      <div className="toolbar1">

        <SearchBar
          value={searchQuery}
          onChange={setSearchQuery}
          placeholder="Search collections..."
        />

      </div>

      {successMessage && <div className="success-message">{successMessage}</div>}

      {filteredCollections.length === 0 && !successMessage ? (
        <div className="no-collections-message">No collections found.</div>
      ) : (
        <div className="collection-grid">
          {filteredCollections.map(collection => (
            <CollectionCard
              key={collection.id}
              collection={collection}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}

    </div>
  );
};

export default CollectionList;