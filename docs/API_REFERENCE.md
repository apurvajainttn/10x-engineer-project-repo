# API Reference

This document provides detailed information about the available API endpoints in the `api.py` file for the PromptLab API.

## Endpoints Overview

- **Health Check**
- **Prompts**: CRUD operations for prompts.
- **Collections**: CRUD operations for collections.

---

## Health Check

### GET /health

- **Description**: Performs a health check for the API service.
- **Parameters**: None
- **Request body**: None
- **Response format**: JSON
- **Request example**:
  ```sh
  curl http://<api-url>/health
  ```
- **Response example**:
  ```json
  {
    "status": "healthy",
    "version": "1.0.0"
  }
  ```
- **Error codes**: None expected
- **Error response formats**: None expected
- **Authentication notes**: None

---

## Prompts

### GET /prompts

- **Description**: Retrieves a list of prompts optionally filtered by collection and search query.
- **Parameters**:
  - `collection_id` (Optional): Filter prompts by collection ID.
  - `search` (Optional): Filter prompts by search keyword.
- **Request body**: None
- **Response format**: JSON
- **Request example**:
  ```sh
  curl "http://<api-url>/prompts?collection_id=123&search=my_query"
  ```
- **Response example**:
  ```json
  {
    "prompts": [...],
    "total": 5
  }
  ```
- **Error codes**: 
  - `500`: Internal server error if accessing storage fails.
- **Error response formats**: JSON with error details.
- **Authentication notes**: None

### GET /prompts/{prompt_id}

- **Description**: Retrieve a specific prompt by its ID.
- **Parameters**: None
- **Request body**: None
- **Response format**: JSON
- **Request example**:
  ```sh
  curl http://<api-url>/prompts/123
  ```
- **Response example**:
  ```json
  {
    "id": "123",
    "title": "Sample Prompt",
    "content": "..."
  }
  ```
- **Error codes**:
  - `404`: Prompt not found
- **Error response formats**: JSON with `detail` of the error.
- **Authentication notes**: None

### POST /prompts

- **Description**: Creates a new prompt.
- **Parameters**: None
- **Request body**: JSON with `PromptCreate` details.
- **Response format**: JSON
- **Request example**:
  ```sh
  curl -X POST http://<api-url>/prompts -H "Content-Type: application/json" -d '{"title": "New Prompt", "description": "This is a new prompt", "collection_id": "1"}'
  ```
- **Response example**:
  ```json
  {
    "id": "new_id",
    "title": "New Prompt",
    "description": "This is a new prompt",
    "collection_id": "1"
  }
  ```
- **Error codes**:
  - `400`: Collection not found
- **Error response formats**: JSON with `detail` of the error.
- **Authentication notes**: None

### PUT /prompts/{prompt_id}

- **Description**: Update an existing prompt by its ID.
- **Parameters**: None
- **Request body**: JSON with `PromptUpdate` details.
- **Response format**: JSON
- **Request example**:
  ```sh
  curl -X PUT http://<api-url>/prompts/123 -H "Content-Type: application/json" -d '{"title": "Updated Title", "content": "Updated Content"}'
  ```
- **Response example**:
  ```json
  {
    "id": "123",
    "title": "Updated Title",
    "content": "Updated Content"
  }
  ```
- **Error codes**:
  - `404`: Prompt not found
  - `400`: Collection not found
- **Error response formats**: JSON with `detail` of the error.
- **Authentication notes**: None

### PATCH /prompts/{prompt_id}

- **Description**: Partially updates a prompt's details.
- **Parameters**: None
- **Request body**: JSON with `PromptPatch` details.
- **Response format**: JSON
- **Request example**:
  ```sh
  curl -X PATCH http://<api-url>/prompts/123 -H "Content-Type: application/json" -d '{"title": "Partially Updated Title"}'
  ```
- **Response example**:
  ```json
  {
    "id": "123",
    "title": "Partially Updated Title"
  }
  ```
- **Error codes**:
  - `404`: Prompt not found
  - `400`: No fields provided for update
  - `400`: Collection not found
- **Error response formats**: JSON with `detail` of the error.
- **Authentication notes**: None

### DELETE /prompts/{prompt_id}

- **Description**: Delete a prompt by its ID.
- **Parameters**: None
- **Request body**: None
- **Response format**: None
- **Request example**:
  ```sh
  curl -X DELETE http://<api-url>/prompts/123
  ```
- **Error codes**:
  - `404`: Prompt not found
- **Error response formats**: JSON with `detail` of the error.
- **Authentication notes**: None

---

## Collections

### GET /collections

- **Description**: List all collections.
- **Parameters**: None
- **Request body**: None
- **Response format**: JSON
- **Request example**:
  ```sh
  curl http://<api-url>/collections
  ```
- **Response example**:
  ```json
  {
    "collections": [...],
    "total": 10
  }
  ```
- **Error codes**: 
  - `500`: Internal server error if accessing storage fails.
- **Error response formats**: JSON with error details.
- **Authentication notes**: None

### GET /collections/{collection_id}

- **Description**: Retrieve a collection by ID.
- **Parameters**: None
- **Request body**: None
- **Response format**: JSON
- **Request example**:
  ```sh
  curl http://<api-url>/collections/123
  ```
- **Response example**:
  ```json
  {
    "id": "123",
    "name": "Collection Name",
    "description": "A test collection"
  }
  ```
- **Error codes**:
  - `404`: Collection not found
- **Error response formats**: JSON with `detail` of the error.
- **Authentication notes**: None

### POST /collections

- **Description**: Create a new collection.
- **Parameters**: None
- **Request body**: JSON with `CollectionCreate` details.
- **Response format**: JSON
- **Request example**:
  ```sh
  curl -X POST http://<api-url>/collections -H "Content-Type: application/json" -d '{"name": "New Collection", "description": "A test collection"}'
  ```
- **Response example**:
  ```json
  {
    "id": "new_id",
    "name": "New Collection",
    "description": "A test collection"
  }
  ```
- **Error codes**: 
  - `500`: Internal server error if accessing storage fails.
- **Error response formats**: JSON with error details.
- **Authentication notes**: None

### DELETE /collections/{collection_id}

- **Description**: Delete a collection by ID and clear related prompts.
- **Parameters**: None
- **Request body**: None
- **Response format**: None
- **Request example**:
  ```sh
  curl -X DELETE http://<api-url>/collections/123
  ```
- **Error codes**:
  - `404`: Collection not found
- **Error response formats**: JSON with `detail` of the error.
- **Authentication notes**: None

---