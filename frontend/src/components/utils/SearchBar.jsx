import React from 'react';
import './styles/SearchBar.css';

const SearchBar = ({ value, onChange, placeholder = 'Search prompts...' }) => {

  return (
    <div className="search-bar-container">

      <span className="search-icon">🔍</span>

      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="search-bar"
      />

    </div>
  );

};

export default SearchBar;