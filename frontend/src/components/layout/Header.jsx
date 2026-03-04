import React from 'react';
import './styles/Header.css';
import PromptLabLogo from '../../assets/PromptLabLogo.png';

const Header = ({ onToggleSidebar }) => {
  return (
    <header className="app-header">
      <div className="header-left">
        <button className="menu-toggle" onClick={onToggleSidebar}>
          ☰
        </button>
        <div className="logo" onClick={redirectToHome} style={{ cursor: 'pointer' }}>
          <img src={PromptLabLogo} alt="PromptLab Logo" className="header-logo" />
        </div>
      </div>
    </header>
  );
};

const redirectToHome = () => {
  window.location.href = '/';
};

export default Header;