# Tagging System Specifications

## Overview of Tagging Feature
The tagging feature allows users to organize and manage their AI prompts efficiently by attaching descriptive tags. This system will enable users to categorize prompts, making it easier to search, filter, and group related prompts. Tags will be flexible and user-defined, allowing for a customizable organization strategy that fits various workflows.

## User Stories with Acceptance Criteria

### Story 1: Add Tags to a Prompt
- **As a** user
- **I want** to add one or more tags to a prompt
- **So that** I can categorize and easily find related prompts later
  
  - **Acceptance Criteria:**
    - Users can add multiple tags to an individual prompt.
    - Tags can be added when creating a new prompt or updating an existing one.
    - The system prevents duplicate tags on the same prompt.

### Story 2: Remove Tags from a Prompt
- **As a** user
- **I want** to remove tags from a prompt
- **So that** I can update the prompt's categorization or correct mistakes

  - **Acceptance Criteria:**
    - Users can remove one or more tags from an individual prompt.
    - Users receive confirmation before a tag is removed.

### Story 3: Search Prompts by Tags
- **As a** user
- **I want** to search prompts using tags
- **So that** I can find prompts associated with specific topics or categories

  - **Acceptance Criteria:**
    - Users can search and filter prompts based on single or multiple tags.
    - The search results are updated in real-time as tags are added or removed.

### Story 4: Tag Management
- **As a** user
- **I want** to manage the list of available tags
- **So that** I can ensure consistency and clarity in tag usage

  - **Acceptance Criteria:**
    - Users can view all existing tags.
    - Users can delete tags that are no longer needed, but with a confirmation prompt.
    - Users can see a count of how many times a tag is used.

## Data Model Changes Needed
- Add a `tags` field to the Prompt model:
  ```python
  class Prompt(Base):
      # ... existing fields ...
      tags: List[str]
  ```
- Create a Tag entity to track usage and manage tags:
  ```python
  class Tag(Base):
      name: str
      prompt_count: int
  ```

## API Endpoint Specifications

### Endpoint: Add Tags to Prompt
- **Method:** POST
- **URL:** /prompts/{prompt_id}/tags
- **Request Body:**
  ```json
  {
    "tags": ["tag1", "tag2", ...]
  }
  ```
- **Response:**
  - 200 OK: Tags added successfully
  - 400 Bad Request: Invalid tags or duplicate

### Endpoint: Remove Tags from Prompt
- **Method:** DELETE
- **URL:** /prompts/{prompt_id}/tags
- **Request Body:**
  ```json
  {
    "tags": ["tag1", "tag2", ...]
  }
  ```
- **Response:**
  - 200 OK: Tags removed successfully
  - 404 Not Found: Tags not found on prompt

### Endpoint: Search Prompts by Tags
- **Method:** GET
- **URL:** /prompts/search?tags=tag1,tag2
- **Response:**
  - 200 OK: List of prompts matching tags

### Endpoint: Manage Tags
- **Method:** GET
- **URL:** /tags
- **Response:**
  - 200 OK: List of all tags with usage count

## Search/Filter Requirements
- Implement a search functionality that allows filtering prompts by tags.
- Allow AND/OR logic for combining multiple tags in a search query.
- Optimize for real-time updates to the list of available prompts as tags are modified.
