import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Layout from './components/layout/Layout';
import PromptList from './components/prompt/PromptList';
import PromptForm from './components/prompt/PromptForm';
import EditPrompt from './components/prompt/EditPrompt';
import CollectionForm from './components/collection/CollectionForm';
import CollectionList from './components/collection/CollectionList';
import PromptDetail from './components/prompt/PromptDetail';
import HomePage from './components/homepage/HomePage'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="browse-prompts" element={<PromptList />} />
          <Route path="create-prompt" element={<PromptForm />} />
          <Route path="edit-prompt/:id" element={<EditPrompt />} />
          <Route path="create-collections" element={<CollectionForm />} />
          <Route path="browse-collections" element={<CollectionList />} />
          <Route path="/prompt/:promptId" element={<PromptDetail />} />
          {/* Add routes for other components like PromptDetail, etc. */}
        </Route>
      </Routes>
    </Router>
  );
}

export default App;