import React from 'react';
import { Link } from 'react-router-dom';
import './styles/Sidebar.css';

const Sidebar = ({ isVisible, onClose }) => {

  const handleLinkClick = () => {
    if (onClose) {
      onClose();
    }
  };

  return (
    <aside className={`app-sidebar ${isVisible ? 'visible' : 'hidden'}`}>
      <nav className="sidebar-navigation">
        <ul>
          <li><Link to="/dashboard" onClick={handleLinkClick}>View All Prompts</Link></li>
          <li><Link to="/create-prompt" onClick={handleLinkClick}>Create New Prompt</Link></li>
          <li><Link to="/create-collections" onClick={handleLinkClick}>Create Collections</Link></li>
          <li><Link to="/list-collections" onClick={handleLinkClick}>List Collections</Link></li>
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;