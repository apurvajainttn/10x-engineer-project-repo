import pytest
from fastapi.testclient import TestClient

def test_add_single_tag_to_prompt(client: TestClient):
    # Set up the expected tags
    expected_tags = ["tag1", "tag2"]
    
    # Prepare the prompt creation data
    prompt_data = {
        "title": "Test Prompt",
        "content": "Content for test",
        "tags": expected_tags
    }
    
    # Create the prompt using the API
    response = client.post("/prompts", json=prompt_data)
    assert response.status_code == 201
    created_prompt = response.json()
    
    # Verify prompt is stored immediately after creation
    assert set(created_prompt['tags']) == set(expected_tags)
    
    # Arrange: Setup initial state
    prompt_id = created_prompt["id"]

    # Act: Perform the API call
    response = client.post(f"/prompts/{prompt_id}/tags", json={"tags": ["tag3"]})

    # Assert: Validate results
    assert response.status_code == 200
    assert response.json() == {"message": "Tags added: ['tag3']"}


def test_add_multiple_tags_to_prompt(client: TestClient):
    # Set up the expected tags
    expected_tags = ["tag1", "tag2"]
    
    # Prepare the prompt creation data
    prompt_data = {
        "title": "Test Prompt",
        "content": "Content for test",
        "tags": expected_tags
    }
    
    # Create the prompt using the API
    response = client.post("/prompts", json=prompt_data)
    assert response.status_code == 201
    created_prompt = response.json()
    
    # Verify prompt is stored immediately after creation
    assert set(created_prompt['tags']) == set(expected_tags)
    
    # Arrange: Setup initial state
    prompt_id = created_prompt["id"]

    # Act
    response = client.post(f"/prompts/{prompt_id}/tags", json={"tags": ["tag3", "tag4"]})

    # Extract the tags from the response message
    response_tags = eval(response.json()["message"].split(": ")[1])

    # Assert
    assert response.status_code == 200
    assert sorted(response_tags) == sorted(["tag3", "tag4"])


def test_add_duplicate_tags_to_prompt(client: TestClient):
    # Set up the expected tags
    expected_tags = ["tag1", "tag2"]
    
    # Prepare the prompt creation data
    prompt_data = {
        "title": "Test Prompt",
        "content": "Content for test",
        "tags": expected_tags
    }
    
    # Create the prompt using the API
    response = client.post("/prompts", json=prompt_data)
    assert response.status_code == 201
    created_prompt = response.json()
    
    # Verify prompt is stored immediately after creation
    assert set(created_prompt['tags']) == set(expected_tags)
    
    # Arrange: Setup initial state
    prompt_id = created_prompt["id"]

    # Act
    response = client.post(f"/prompts/{prompt_id}/tags", json={"tags": ["tag1", "tag1"]})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Duplicate tags were provided"}

def test_add_tags_to_non_existing_prompt(client: TestClient):
    # Arrange: Use a prompt ID that does not exist.
    invalid_prompt_id = "non_existent_id"

    # Act: Try to add tags to a non-existent prompt.
    response = client.post(f"/prompts/{invalid_prompt_id}/tags", json={"tags": ["new_tag"]})

    # Assert: Verify that the response indicates the prompt was not found.
    assert response.status_code == 404
    assert response.json() == {"detail": "Prompt not found"}

def test_create_prompt_with_tags(client: TestClient):
    # Arrange: Create a new prompt with tags
    prompt_data = {
        "title": "New Prompt",
        "content": "This is a new prompt content.",
        "tags": ["tag1", "tag2"]
    }

    # Act: Make API call to create prompt with tags
    response = client.post("/prompts", json=prompt_data)

    # Assert: Check if the tags are added successfully
    assert response.status_code == 201
    data = response.json()
    assert "tags" in data
    assert set(data["tags"]) == {"tag1", "tag2"}


def test_create_prompt_with_duplicate_tags(client: TestClient):
    # Arrange: Prepare prompt data with duplicate tags
    prompt_data = {
        "title": "Prompt with Duplicates",
        "content": "Testing duplicate tags",
        "tags": ["tag1", "tag1", "tag2"]
    }

    # Act: Make API call
    response = client.post("/prompts", json=prompt_data)

    # Assert: Ensure tags are stored as unique
    assert response.status_code == 201
    data = response.json()
    assert "tags" in data
    assert set(data["tags"]) == {"tag1", "tag2"}

def test_remove_single_tag_from_prompt(client: TestClient):
    # Set up the expected tags
    expected_tags = ["old_tag"]
    
    # Prepare the prompt creation data
    prompt_data = {
        "title": "Test Prompt",
        "content": "Content for test",
        "tags": expected_tags
    }
    
    # Create the prompt using the API
    response = client.post("/prompts", json=prompt_data)
    assert response.status_code == 201
    created_prompt = response.json()
    
    # Verify prompt is stored immediately after creation
    assert set(created_prompt['tags']) == set(expected_tags)
    
    # Arrange: Setup initial state
    prompt_id = created_prompt["id"]
    
    # Act
    response = client.request(
        method="DELETE",
        url=f"/prompts/{prompt_id}/tags",
        json={"tags": ["old_tag"]},
        headers={"Content-Type": "application/json"}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Tags removed successfully"}

def test_remove_multiple_tags_from_prompt(client: TestClient):
    # Set up the expected tags
    expected_tags = ["old_tag", "another_tag"]
    
    # Prepare the prompt creation data
    prompt_data = {
        "title": "Test Prompt",
        "content": "Content for test",
        "tags": expected_tags
    }
    
    # Create the prompt using the API
    response = client.post("/prompts", json=prompt_data)
    assert response.status_code == 201
    created_prompt = response.json()
    
    # Verify prompt is stored immediately after creation
    assert set(created_prompt['tags']) == set(expected_tags)
    
    # Arrange: Setup initial state
    prompt_id = created_prompt["id"]

    # Act
    response = client.request(
        method="DELETE",
        url=f"/prompts/{prompt_id}/tags",
        json={"tags": ["old_tag", "another_tag"]},
        headers={"Content-Type": "application/json"}
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Tags removed successfully"}

def test_remove_nonexistent_tag_from_prompt(client: TestClient):
    # Set up the expected tags
    expected_tags = ["old_tag", "another_tag"]
    
    # Prepare the prompt creation data
    prompt_data = {
        "title": "Test Prompt",
        "content": "Content for test",
        "tags": expected_tags
    }
    
    # Create the prompt using the API
    response = client.post("/prompts", json=prompt_data)
    assert response.status_code == 201
    created_prompt = response.json()
    
    # Verify prompt is stored immediately after creation
    assert set(created_prompt['tags']) == set(expected_tags)
    
    # Arrange: Setup initial state
    prompt_id = created_prompt["id"]
    
    # Act
    response = client.request(
        method="DELETE",
        url=f"/prompts/{prompt_id}/tags",
        json={"tags": ["nonexistent_tag"]},
        headers={"Content-Type": "application/json"}
    )
    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Tags not found on prompt"}

def test_remove_tags_from_non_existing_prompt(client: TestClient):
    # Arrange: Use a prompt ID that does not exist.
    invalid_prompt_id = "non_existent_id"

    # Act: Try to remove tags from a non-existent prompt.
    response = client.request(
        method="DELETE",
        url=f"/prompts/{invalid_prompt_id}/tags",
        json={"tags": ["tag1"]},
        headers={"Content-Type": "application/json"}
    )

    # Assert: Verify that the response indicates the prompt was not found.
    assert response.status_code == 404
    assert response.json() == {"detail": "Prompt not found"}

def test_search_prompts_by_tags(client: TestClient):
    # Set up the expected tags
    expected_tags = ["tag1", "tag2"]
    
    # Prepare the prompt creation data
    prompt_data = {
        "title": "Test Prompt",
        "content": "Content for test",
        "tags": expected_tags
    }
    
    # Create the prompt using the API
    response = client.post("/prompts", json=prompt_data)
    assert response.status_code == 201
    created_prompt = response.json()
    
    # Verify prompt is stored immediately after creation
    assert set(created_prompt['tags']) == set(expected_tags)
    
    # Test for successful retrieval of prompts
    tag_query = ",".join(expected_tags)
    response = client.get(f"/prompts/search?tags={tag_query}")
    assert response.status_code == 200
    data = response.json()
    assert data['total'] == 1
    assert data['prompts'][0]['title'] == "Test Prompt"
    
    # Test for retrieval with no matching tags
    response = client.get("/prompts/search?tags=nonexistent")
    assert response.status_code == 200
    data = response.json()
    assert data['total'] == 0
    
    # Clean up by deleting the created prompt
    client.delete(f"/prompts/{created_prompt['id']}")

def test_list_tags(client: TestClient):
        """Test retrieving all tags.

        Args:
            client (TestClient): The HTTP client for testing.

        Asserts:
            The status code is 200.
            A list of tags is returned.
        """
        response = client.get("/tags")
        assert response.status_code == 200
        data = response.json()
        assert type(data) == list

def test_delete_tag_success(client: TestClient):
        """Test successful deletion of a tag.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 204 after a tag is deleted.
            The tag is no longer listed in the prompts.
        """
        # Add a prompt with tags
        prompt_data = {"title": "Sample Title", "content": "Sample Content", "tags": ["to-delete", "other-tag"]}
        client.post("/prompts", json=prompt_data)

        # Determine which tag to remove
        tag_to_remove = "to-delete"
        del_response = client.delete(f"/tags/{tag_to_remove}")

        # Assert successful deletion
        assert del_response.status_code == 204

        # Ensure tag is removed from all prompts
        prompts_resp = client.get(f"/prompts")
        prompts_data = prompts_resp.json()
        for prompt in prompts_data["prompts"]:
            assert tag_to_remove not in prompt["tags"]

def test_delete_tag_not_found(client: TestClient):
        """Test deleting a non-existent tag.

        Args:
            client (TestClient): The HTTP client for testing.

        Asserts:
            The status code is 404 when the tag does not exist.
        """
        non_existent_tag = "nonexistent"
        del_response = client.delete(f"/tags/{non_existent_tag}")
        
        # Assert proper error handling
        assert del_response.status_code == 404
        assert "Tag not found" in del_response.json()["detail"]