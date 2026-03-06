import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getPrompt } from '../../api/prompts';
import LoadingSpinner from '../utils/LoadingSpinner';
import ErrorMessage from '../utils/ErrorMessage';
import './styles/PromptDetail.css';
import BackButton from '../utils/BackButton';

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
        console.log("Error to load prompt details", err)
        setError('Failed to load prompt details.');
      } finally {
        setLoading(false);
      }

    };

    fetchPrompt();

  }, [promptId]);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;
  if (!prompt) return <div>No prompt details available.</div>;

  return (
    <div className="prompt-detail-page">

      <div className="prompt-detail-container">

        <div className="prompt-detail-header">

          <BackButton />

          <div className="header-text">
            <h1>Prompt Details</h1>
            <p>View and manage your AI prompt</p>
          </div>

        </div>

        <div className="prompt-detail-card">

          <h2 className="prompt-title">{prompt.title}</h2>

          <p className="prompt-description">{prompt.description}</p>

          <div className="prompt-content-box">
            <pre>{prompt.content}</pre>
          </div>

          {prompt.tags?.length > 0 && (
            <div className="prompt-tags">

              <span className="tag-label">Tags:</span>

              {prompt.tags.map((tag, index) => (
                <span key={index} className="tag">
                  {tag}
                </span>
              ))}

            </div>
          )}

        </div>

      </div>

    </div>
  );
};

export default PromptDetail;