import React from 'react';

const CollectionList = ({ collections }) => {
  return (
    <div className="collection-list">
      <ul>
        {collections.map(collection => (
          <li key={collection.id}>{collection.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default CollectionList;
