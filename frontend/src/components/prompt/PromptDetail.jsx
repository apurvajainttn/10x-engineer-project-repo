import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getPrompt } from '../../api/prompts'; // Assume this function fetches a prompt by its ID

const PromptDetail = () => {
  const { promptId } = useParams();
  const [prompt, setPrompt] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPrompt = async () => {
      try {
        const promptData = await getPrompt(promptId);
        setPrompt(promptData);
      } catch (err) {
        console.log("Logging Error", err)
        setError('Failed to load prompt details.');
      } finally {
        setLoading(false);
      }
    };
    fetchPrompt();
  }, [promptId]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  if (!prompt) {
    return <div>No prompt details available.</div>;
  }

  return (
    <div className="prompt-detail">
      <h1>{prompt.title}</h1>
      <p>{prompt.description}</p>
      <p>{prompt.content}</p>
      <p>Tags: {prompt.tags.join(', ')}</p>
      {/* Add more detailed information about the prompt */}
    </div>
  );
};

export default PromptDetail;
