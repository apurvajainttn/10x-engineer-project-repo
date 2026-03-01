import { fetchWrapper } from './client';

async function getPrompts() {
  return fetchWrapper('/prompts');
}

async function getPrompt(id) {
  return fetchWrapper(`/prompts/${id}`);
}

async function createPrompt(data) {
  return fetchWrapper('/prompts', {
    method: 'POST',
    body: JSON.stringify(data)
  });
}

async function updatePrompt(id, data) {
  return fetchWrapper(`/prompts/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data)
  });
}

async function deletePrompt(id) {
  return fetchWrapper(`/prompts/${id}`, {
    method: 'DELETE'
  });
}

export {
  getPrompts,
  getPrompt,
  createPrompt,
  updatePrompt,
  deletePrompt
};
