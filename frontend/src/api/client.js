const BASE_URL = 'http://localhost:8000';

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

    // Handle 204 No Content
    if (response.status === 204) {
      return { status: 204, message: 'No Content' }; // Or return null or custom object
    }

    return response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

export { fetchWrapper };
