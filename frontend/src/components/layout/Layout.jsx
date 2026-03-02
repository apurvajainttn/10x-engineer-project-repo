import React, { useState } from 'react';
import Header from './Header';
import Sidebar from './Sidebar';
import './styles/Layout.css';
import { Outlet } from 'react-router-dom';

const Layout = () => {
  const [isSidebarVisible, setSidebarVisible] = useState(false);

  const toggleSidebar = () => {
    setSidebarVisible(!isSidebarVisible);
  };

   const closeSidebar = () => {
    setSidebarVisible(false);
  };

  return (
    <div className="app-layout">
      <Header onToggleSidebar={toggleSidebar} />
      <div className="layout-body">
        <Sidebar isVisible={isSidebarVisible} onClose={closeSidebar} />
        <main className="main-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;