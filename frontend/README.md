# PromptLab Frontend

PromptLab is a web application designed to manage, organize, and test AI prompts efficiently. This frontend project is built with React and Vite, ensuring a fast and modern user interface experience.

## Getting Started

These instructions will help you set up the frontend development environment.

### Prerequisites

- Node.js 18+ and npm (Node Package Manager)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
   
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
   
3. Install the dependencies:
   ```bash
   npm install
   ```

### Development

To run the app in development mode:

```bash
npm run dev
```

This will start the development server, and you can view the application by navigating to http://localhost:5173 in your web browser.

## Configuration

The frontend communicates with the backend via APIs. The base URL for these APIs is defined in `src/api/client.js`. This URL can be updated based on your local or production backend environment setup.

### API Base URL

Currently, the `BASE_URL` is set to:

```javascript
const BASE_URL = 'http://localhost:8000';
```

You should modify this URL in `src/api/client.js` to match your backend configuration when setting up the application locally.

## Project Structure

- **src/**: Source directory for frontend components and assets.
  - **components/**: Contains all React components.
  - **api/**: Contains API service modules for handling HTTP requests.
  - **assets/**: Image and media assets.
  - **styles/**: CSS styles for components.