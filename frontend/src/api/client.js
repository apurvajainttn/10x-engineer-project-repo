const BASE_URL = 'http://localhost:8000/api';

async function fetchWrapper(url, options = {}) {
  try {
    const response = await fetch(`${BASE_URL}${url}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Something went wrong');
    }

    // Resolve with JSON data
    return response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

export { fetchWrapper };
