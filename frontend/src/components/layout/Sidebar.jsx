import React from 'react';
import { Link } from 'react-router-dom';
import './styles/Sidebar.css';
import viewPromptsIcon from "../../assets/ViewPromptsIcon.svg";
import createPromptIcon from "../../assets/CreatePromptIcon.svg";
import createCollectionIcon from "../../assets/CreateCollectionIcon.svg";
import listCollectionsIcon from "../../assets/ViewCollectionsIcon.svg";
import homeIcon from "../../assets/HomeIcon.svg";
import promptLabLogo from "../../assets/PromptLabLogo.png";

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
          <li><Link to="/" onClick={handleLinkClick}><img src={homeIcon} width={24} height={24} alt="Home Icon" />Home</Link></li>
          <li><Link to="/browse-prompts" onClick={handleLinkClick}><img src={viewPromptsIcon} width={24} height={24} />Browse Prompts</Link></li>
          <li><Link to="/create-prompt" onClick={handleLinkClick}><img src={createPromptIcon} width={24} height={24} />Create New Prompt</Link></li>
          <li><Link to="/browse-collections" onClick={handleLinkClick}><img src={listCollectionsIcon} width={24} height={24} />Browse Collections</Link></li>
          <li><Link to="/create-collections" onClick={handleLinkClick}><img src={createCollectionIcon} width={24} height={24} />Create New Collection</Link></li>
        </ul>
      </nav>
      <div className="sidebar-footer">
        <img src={promptLabLogo} alt="PromptLab Logo" className="prompt-lab-logo" />
      </div>
    </aside>
  );
};

export default Sidebar;