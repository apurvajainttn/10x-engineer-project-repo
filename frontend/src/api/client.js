const BASE_URL = 'https://fuzzy-fortnight-5g6rw9p9vgqwfvg4x-8000.app.github.dev';

async function fetchWrapper(url, options = {}) {
  try {
    const isBodyRequest = options.body !== undefined;

    const response = await fetch(`${BASE_URL}${url}`, {
      ...options,
      headers: {
        ...(isBodyRequest && { 'Content-Type': 'application/json' }),
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Something went wrong');
    }

    return response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

export { fetchWrapper };
