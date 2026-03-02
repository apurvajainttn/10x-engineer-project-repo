import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import PromptForm from './PromptForm';
import { getPrompt } from '../../api/prompts';
import LoadingSpinner from '../../../utils/LoadingSpinner';
import ErrorMessage from '../../../utils/ErrorMessage';

const EditPrompt = () => {
  const { id } = useParams();
  const [initialData, setInitialData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPrompt = async () => {
      try {
        const data = await getPrompt(id);
        setInitialData(data);
        setLoading(false);
      } catch (err) {
        setError(err);
        setLoading(false);
      }
    };
    fetchPrompt();
  }, [id]);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error.message} />;
  if (!initialData) return null;

  return <PromptForm initialData={initialData} isEditing={true} />;
};

export default EditPrompt;