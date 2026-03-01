import { fetchWrapper } from './client';

async function getCollections() {
  return fetchWrapper('/collections');
}

async function createCollection(data) {
  return fetchWrapper('/collections', {
    method: 'POST',
    body: JSON.stringify(data)
  });
}

async function deleteCollection(id) {
  return fetchWrapper(`/collections/${id}`, {
    method: 'DELETE'
  });
}

export {
  getCollections,
  createCollection,
  deleteCollection
};
