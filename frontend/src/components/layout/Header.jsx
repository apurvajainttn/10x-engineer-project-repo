import React from 'react';
import './styles/Header.css';
import PromptLabLogo from '../../assets/PromptLabLogo.png';
import { useNavigate } from 'react-router-dom';
import Button from '../utils/Button';

const Header = ({ onToggleSidebar }) => {
  const navigate = useNavigate();

  const redirectToHome = () => {
    navigate('/');
  };

  return (
    <header className="app-header">
      <div className="header-left">
        <Button className="menu-toggle" onClick={onToggleSidebar}>
          ☰
        </Button>
        <div className="logo" onClick={redirectToHome} style={{ cursor: 'pointer' }}>
          <img src={PromptLabLogo} alt="PromptLab Logo" className="header-logo" />
        </div>
      </div>
    </header>
  );
};

export default Header;