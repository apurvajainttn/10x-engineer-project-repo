// frontend/src/components/collection/CollectionList.jsx
import React, { useState, useEffect } from 'react';
import { getCollections, deleteCollection } from '../../api/collections'; // Import collection API functions
import CollectionCard from './CollectionCard'; // Assume CollectionCard is where individual collections are rendered
import LoadingSpinner from '../../../utils/LoadingSpinner';
import ErrorMessage from '../../../utils/ErrorMessage';

const CollectionList = () => {
  const [collections, setCollections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');

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
          
          // Clear message after 3 seconds and check if no collections left
          if (collections.length === 0) {
            setError({ message: 'No collections found.' });
          }
        }, 3000);
      } else {
        throw new Error('Failed to delete the collection');
      }
    } catch (err) {
      setError(err);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (error && !successMessage) return <ErrorMessage message={error.message} />;

  return (
    <div className="collection-list">
      {successMessage && <div className="success-message">{successMessage}</div>}
      {collections.length === 0 && !successMessage ? (
        <div className="no-collections-message">No collections found.</div>
      ) : (
        collections.map(collection => (
          <CollectionCard key={collection.id} collection={collection} onDelete={handleDelete} />
        ))
      )}
    </div>
  );
};

export default CollectionList;