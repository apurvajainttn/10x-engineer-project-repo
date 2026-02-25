"""API tests for PromptLab

These tests verify the API endpoints work correctly.
Students should expand these tests significantly in Week 3.
"""

import pytest
from fastapi.testclient import TestClient

class TestHealth:
    """Tests for health endpoint."""
    
    def test_health_check(self, client: TestClient):
        """Test the health check endpoint for application status.

        Args:
            client (TestClient): The HTTP client for testing.

        Asserts:
            The status code is 200.
            The response data contains a 'status' field with the value 'healthy' and includes the application version.
        """
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestPrompts:
    """Tests for prompt endpoints."""
    
    def test_create_prompt(self, client: TestClient, sample_prompt_data):
        """Test the creation of a new prompt.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 201.
            The response data contains correct prompt details.
        """
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_prompt_data["title"]
        assert data["content"] == sample_prompt_data["content"]
        assert "id" in data
        assert "created_at" in data
    
    def test_list_prompts_empty(self, client: TestClient):
        """Test listing prompts when there are no prompts.

        Args:
            client (TestClient): The HTTP client for testing.

        Asserts:
            The status code is 200.
            The list of prompts is empty and total count is 0.
        """
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert data["prompts"] == []
        assert data["total"] == 0
    
    def test_list_prompts_with_data(self, client: TestClient, sample_prompt_data):
        """Test listing prompts when prompts exist.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 200.
            The list contains prompts.
        """
        # Create a prompt first
        client.post("/prompts", json=sample_prompt_data)
        
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) == 1
        assert data["total"] == 1
    
    def test_get_prompt_success(self, client: TestClient, sample_prompt_data):
        """Test retrieving a prompt by ID when it exists.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 200.
            The response data contains the correct prompt ID.
        """
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        response = client.get(f"/prompts/{prompt_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == prompt_id
    
    def test_get_prompt_not_found(self, client: TestClient):
        """Test retrieving a non-existent prompt.

        Args:
            client (TestClient): The HTTP client for testing.

        Asserts:
            The status code is 404.
        
        NOTE: This test now passes as Bug #1 is fixed!
        The API returns 404 now.
        """
        response = client.get("/prompts/nonexistent-id")
        # This should be 404.
        assert response.status_code == 404  # Passing now as bug is fixed
    
    def test_delete_prompt(self, client: TestClient, sample_prompt_data):
        """Test deleting an existing prompt.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 204 upon successful deletion.
            The prompt cannot be retrieved afterwards.
        """
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Delete it
        response = client.delete(f"/prompts/{prompt_id}")
        assert response.status_code == 204
        
        # Verify it's gone
        get_response = client.get(f"/prompts/{prompt_id}")
        # Note: This might fail due to Bug #1
        assert get_response.status_code in [404, 500]  # 404 after fix
    
    def test_update_prompt(self, client: TestClient, sample_prompt_data):
        """Test updating an existing prompt.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 200 after update.
            The prompt's updated fields are correct.
        """
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_updated_at = create_response.json()["updated_at"]
        
        # Update it
        updated_data = {
            "title": "Updated Title",
            "content": "Updated content for the prompt",
            "description": "Updated description"
        }
        
        import time
        time.sleep(0.1)  # Small delay to ensure timestamp would change
        
        response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        
        # NOTE: This assertion now passes as Bug #2 is fixed!
        # The updated_at should be different from original
        assert data["updated_at"] != original_updated_at  # Uncommented after fix
    
    def test_sorting_order(self, client: TestClient):
        """Test that prompts are sorted newest first.

        Args:
            client (TestClient): The HTTP client for testing.

        Asserts:
            The newest prompt is listed first based on the creation timestamp.
        
        Fixed: Bug #3 has been fixed, and the test now passes. Prompts are correctly
        sorted in descending order (newest first) when retrieved from the API.
        """
        import time
        
        # Create prompts with delay
        prompt1 = {"title": "First", "content": "First prompt content"}
        prompt2 = {"title": "Second", "content": "Second prompt content"}
        
        client.post("/prompts", json=prompt1)
        time.sleep(0.1)
        client.post("/prompts", json=prompt2)
        
        response = client.get("/prompts")
        prompts = response.json()["prompts"]
        
        # Newest (Second) should be first
        assert prompts[0]["title"] == "Second"  # Passes now as Bug #3 is fixed

    def test_partial_update_prompt(self, client: TestClient, sample_prompt_data):
        """Test partially updating a prompt.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 200 for successful partial updates.
            The status code is 400 if no fields are provided for update.
        """
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_updated_at = create_response.json()["updated_at"]
        
        # Update it
        updated_data = {
            "title": "Updated Title",
        }
        
        import time
        time.sleep(0.1)  # Small delay to ensure timestamp would change
        
        response = client.patch(f"/prompts/{prompt_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["updated_at"] != original_updated_at 

        # Testing with no update data
        new_updated_data = {}
        response = client.patch(f"/prompts/{prompt_id}", json=new_updated_data)
        assert response.status_code == 400
        assert response.json()["detail"] == "No fields provided for update"

    def test_filter_prompts_by_collection(self, client: TestClient, sample_prompt_data, sample_collection_data):
        """Test listing prompts filtered by collection ID.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.
            sample_collection_data (dict): Sample data for creating a collection.

        Asserts:
            The status code is 200.
            Prompts are correctly filtered by collection ID.
        """
        # Create collection and prompt
        collection_response = client.post("/collections", json=sample_collection_data)
        collection_id = collection_response.json()["id"]
        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        client.post("/prompts", json=prompt_data)

        response = client.get(f"/prompts?collection_id={collection_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) == 1
        assert data["prompts"][0]["collection_id"] == collection_id

    def test_search_prompts(self, client: TestClient, sample_prompt_data):
        """Test searching for prompts by title.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 200.
            The search returns prompts matching the title.
        """
        # Create a prompt first
        client.post("/prompts", json=sample_prompt_data)

        # Search by title
        search_term = sample_prompt_data["title"]
        response = client.get(f"/prompts?search={search_term}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) > 0
        assert search_term in [prompt["title"] for prompt in data["prompts"]]

    def test_create_prompt_without_title(self, client: TestClient, sample_prompt_data):
        """Test creating a prompt without a title.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 422 due to validation failure.
        """
        incomplete_data = sample_prompt_data.copy()
        incomplete_data.pop("title", None)  # Remove title from data
        
        response = client.post("/prompts", json=incomplete_data)
        assert response.status_code == 422

    def test_update_prompt_with_nonexistent_collection(self, client: TestClient, sample_prompt_data):
        """Test updating a prompt with a nonexistent collection ID.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 400 when updating with a nonexistent collection ID.
        """
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Attempt to update with a nonexistent collection
        update_data = {"collection_id": "nonexistent-collection-id"}
        response = client.patch(f"/prompts/{prompt_id}", json=update_data)
        assert response.status_code == 400
        assert "Collection not found" in response.json()["detail"]

    def test_special_characters_in_search(self, client: TestClient, sample_prompt_data):
        """Test searching prompts using special characters.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 200.
        """
        # Create a prompt first
        client.post("/prompts", json=sample_prompt_data)
        
        # Use special characters in search
        special_characters = "!@#$%^&*()"
        response = client.get(f"/prompts?search={special_characters}")
        assert response.status_code == 200

    def test_create_prompt_with_invalid_data_types(self, client: TestClient):
        """Test creating a prompt with invalid data types.

        Args:
            client (TestClient): The HTTP client for testing.

        Asserts:
            The status code is 422 due to validation failure on invalid data types.
        """
        invalid_data = {
            "title": 123,  # Should be a string
            "content": True  # Should be a string
        }
        response = client.post("/prompts", json=invalid_data)
        assert response.status_code == 422

    def test_update_prompt_with_invalid_data_types(self, client: TestClient, sample_prompt_data):
        """Test updating a prompt with invalid data types.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 422 due to validation failure on invalid data types.
        """
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Attempt to update with invalid data types
        invalid_update_data = {
            "title": 456  # Should be a string
        }
        response = client.put(f"/prompts/{prompt_id}", json=invalid_update_data)
        assert response.status_code == 422

    def test_sort_prompts_descending(self, client: TestClient, sample_prompt_data):
        """Test sorting prompts in descending order by date.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating prompts.

        Asserts:
            The status code is 200.
            Prompts are sorted in descending order.
        """
        prompt1 = {"title": "First Prompt", "content": "Content for first prompt"}
        prompt2 = {"title": "Second Prompt", "content": "Content for second prompt"}

        # Create prompts
        client.post("/prompts", json=prompt1)
        client.post("/prompts", json=prompt2)

        response = client.get("/prompts?sort=desc")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) == 2
        assert data["prompts"][0]["title"] == "Second Prompt"

    def test_filter_and_sort_prompts_by_collection_descending(self, client: TestClient, sample_prompt_data, sample_collection_data):
        """Test filtering and sorting prompts by collection in descending order.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.
            sample_collection_data (dict): Sample data for creating a collection.

        Asserts:
            The status code is 200.
            Prompts are filtered by collection and sorted in descending order.
        """
        # Create a collection
        collection_response = client.post("/collections", json=sample_collection_data)
        collection_id = collection_response.json()["id"]
        
        # Create prompts within the collection
        prompt1 = {**sample_prompt_data, "title": "Prompt A", "collection_id": collection_id}
        prompt2 = {**sample_prompt_data, "title": "Prompt B", "collection_id": collection_id}
        client.post("/prompts", json=prompt1)
        client.post("/prompts", json=prompt2)

        response = client.get(f"/prompts?collection_id={collection_id}&sort=asc")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) == 2
        assert data["prompts"][0]["title"] == "Prompt B"

    def test_filter_prompts_no_matches(self, client: TestClient, sample_prompt_data):
        """Test filtering prompts with a collection_id that has no matches.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 200.
            No prompts are returned when filtering with a non-matching collection_id.
        """
        # Create a prompt without a collection_id
        client.post("/prompts", json=sample_prompt_data)
        
        # Attempt to filter by a nonexistent collection
        response = client.get("/prompts?collection_id=nonexistent-id")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) == 0

    def test_patch_prompt_with_no_existing_prompt(self, client: TestClient):
        """Test patching a non-existent prompt.

        Args:
            client (TestClient): The HTTP client for testing.

        Asserts:
            The status code is 404 for a prompt that does not exist.
        """
        patch_data = {"title": "Nonexistent Title Update"}
        response = client.patch("/prompts/nonexistent-id", json=patch_data)
        assert response.status_code == 404

    def test_delete_collection_no_effect(self, client: TestClient):
        """Test deleting a collection that affects no prompts.

        Args:
            client (TestClient): The HTTP client for testing.

        Asserts:
            The status code is 404 for a collection that does not exist.
        """
        response = client.delete("/collections/nonexistent-id")
        assert response.status_code == 404

    def test_filter_prompts_invalid_collection_id(self, client: TestClient):
        """Test filtering prompts with an invalid collection_id.

        Args:
            client (TestClient): The HTTP client for testing.

        Asserts:
            The status code is 200.
            No prompts are returned for an invalid collection_id.
        """
        response = client.get("/prompts?collection_id=invalid-id")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) == 0

    def test_search_prompts_with_no_results(self, client: TestClient, sample_prompt_data):
        """Test searching for prompts that yield no results.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 200.
            No prompts are returned for a search term with no matches.
        """
        client.post("/prompts", json=sample_prompt_data)
        response = client.get("/prompts?search=nonexistent-title")
        assert response.status_code == 200
        assert len(response.json()["prompts"]) == 0

    def test_update_prompt_validation_error(self, client: TestClient, sample_prompt_data):
        """Test updating a prompt and purposely triggering a validation error.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 422 due to validation failure.
        """
        # This uses invalid data intentionally to trigger validation
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        invalid_update_data = {"title": 123}  # Title should be a string
        
        response = client.put(f"/prompts/{prompt_id}", json=invalid_update_data)
        assert response.status_code == 422

    def test_create_prompt_collection_not_found(self, client: TestClient, sample_prompt_data):
        """Test creating a prompt with a non-existent collection ID.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 400 when using a non-existent collection ID.
        """
        # Adjust sample data to include a non-existent collection_id
        prompt_data_with_bad_collection = {**sample_prompt_data, "collection_id": "nonexistent-collection"}
        response = client.post("/prompts", json=prompt_data_with_bad_collection)
        assert response.status_code == 400
        assert response.json()["detail"] == "Collection not found"

    def test_update_prompt_not_found(self, client: TestClient, sample_prompt_data):
        """Test patching a prompt without providing any fields.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 400 if no fields are provided for update.
            The status code is 404 for a non-existent prompt.
        """
        update_data = {"title": "Non-existent Update"}
        response = client.put("/prompts/nonexistent-id", json=update_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt not found"

    def test_patch_prompt_no_fields_provided(self, client: TestClient, sample_prompt_data):
        """Test patching a prompt without providing any fields.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 400 if no fields are provided for update.
            The status code is 404 for a non-existent prompt.
        """
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        # Attempt to patch with no data
        response = client.patch(f"/prompts/{prompt_id}", json={})
        assert response.status_code == 400
        assert response.json()["detail"] == "No fields provided for update"

        # Test non-existent patch
        response = client.patch("/prompts/nonexistent-id", json={})
        assert response.status_code == 404

    def test_delete_non_existent_prompt(self, client: TestClient):
        """Test deleting a prompt that does not exist.

        Args:
            client (TestClient): The HTTP client for testing.

        Asserts:
            The status code is 404 for a prompt that does not exist.
        """
        response = client.delete("/prompts/nonexistent-id")
        assert response.status_code == 404
        assert response.json()["detail"] == "Prompt not found"

    def test_delete_existing_prompt(self, client: TestClient, sample_prompt_data):
        """Ensure the existing prompt can be successfully deleted.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 204 upon successful deletion.
            The prompt cannot be retrieved after deletion.
        """
        # Create a prompt
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        # Delete prompt
        delete_response = client.delete(f"/prompts/{prompt_id}")
        assert delete_response.status_code == 204

        # Ensure prompt no longer exists
        get_response_after_delete = client.get(f"/prompts/{prompt_id}")
        assert get_response_after_delete.status_code == 404

    def test_update_prompt_with_nonexistent_collection_put(self, client: TestClient, sample_prompt_data):
        """Test updating a prompt with a nonexistent collection ID using PUT.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 400 when updating with a nonexistent collection ID.
        """
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
    
        # Attempt to update with a nonexistent collection
        update_data = {"title": "Updated", "collection_id": "nonexistent-collection-id"}
        response = client.put(f"/prompts/{prompt_id}", json=update_data)
        assert response.status_code == 400
        assert "Collection not found" in response.json()["detail"]


class TestCollections:
    """Tests for collection endpoints."""
    
    def test_create_collection(self, client: TestClient, sample_collection_data):
        """Test the creation of a new collection.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_collection_data (dict): Sample data for creating a collection.

        Asserts:
            The status code is 201.
            The response data contains correct collection details.
        """
        response = client.post("/collections", json=sample_collection_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_collection_data["name"]
        assert "id" in data
    
    def test_list_collections(self, client: TestClient, sample_collection_data):
        """Test listing all collections.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_collection_data (dict): Sample data for creating a collection.

        Asserts:
            The status code is 200.
            At least one collection is listed.
        """
        client.post("/collections", json=sample_collection_data)
        
        response = client.get("/collections")
        assert response.status_code == 200
        data = response.json()
        assert len(data["collections"]) == 1
    
    def test_get_collection_not_found(self, client: TestClient):
        """Test retrieving a non-existent collection.

        Args:
            client (TestClient): The HTTP client for testing.

        Asserts:
            The status code is 404.
        """
        response = client.get("/collections/nonexistent-id")
        assert response.status_code == 404
    
    def test_delete_collection_with_prompts(self, client: TestClient, sample_collection_data, sample_prompt_data):
        """Test deleting a collection that has prompts.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_collection_data (dict): Sample data for creating a collection.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is appropriate to indicate prompts are managed correctly.
            Prompts previously linked to the collection have their collection ID set to None.
        
        NOTE: Bug #4 Fixed - prompts will now be assigned collection_id: None, once collection is deleted.
        This test now documents the correct and fixed behavior.
        """
        # Create collection
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        # Create prompt in collection
        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        prompt_response = client.post("/prompts", json=prompt_data)
        prompt_id = prompt_response.json()["id"]
        
        # Delete collection
        client.delete(f"/collections/{collection_id}")
        
        # Bug #4 Fixed
        prompts = client.get("/prompts").json()["prompts"]
        if prompts:
            # Prompts now exists with None collection_id
            for prompt in prompts:
                assert prompt["collection_id"] is None
            # Fixed, collection_id is now set to None

    def test_create_collection_missing_fields(self, client: TestClient):
        """Test creating a collection with missing required fields.

        Args:
            client (TestClient): The HTTP client for testing.

        Asserts:
            The status code is 422 due to validation failure.
        """
        incomplete_data = {"description": "Some description"}  # No name given
        
        response = client.post("/collections", json=incomplete_data)
        assert response.status_code == 422

    def test_delete_non_existent_collection(self, client: TestClient):
        """Test deleting a collection that does not exist.

        Args:
            client (TestClient): The HTTP client for testing.

        Asserts:
            The status code is 404.
        """
        response = client.delete("/collections/nonexistent-id")
        assert response.status_code == 404

    def test_create_collection_with_invalid_data_types(self, client: TestClient):
        """Test creating a collection with invalid data types.

        Args:
            client (TestClient): The HTTP client for testing.

        Asserts:
            The status code is 422 due to validation failure on invalid data types.
        """
        invalid_data = {
            "name": 789,  # Should be a string
            "description": False  # Should be a string
        }
        response = client.post("/collections", json=invalid_data)
        assert response.status_code == 422

    def test_delete_collection_no_association(self, client: TestClient):
        """Test deleting a collection with no associated prompts.

        Args:
            client (TestClient): The HTTP client for testing.

        Asserts:
            The status code is 204 after successful deletion.
        """
        response = client.post("/collections", json={"name": "Isolated Collection", "description": "No prompts here"})
        collection_id = response.json()["id"]
        
        delete_response = client.delete(f"/collections/{collection_id}")
        assert delete_response.status_code == 204

    def test_delete_collection_with_valid_id(self, client: TestClient, sample_collection_data, sample_prompt_data):
        """Ensure 204 status when deleting an existing collection that affects no prompts.

        Args:
            client (TestClient): The HTTP client for testing.
            sample_collection_data (dict): Sample data for creating a collection.
            sample_prompt_data (dict): Sample data for creating a prompt.

        Asserts:
            The status code is 204 after deletion.
            Prompts previously attached to collection have their collection_id set to None.
            The collection is no longer retrievable.
        """
        # Create collection
        response = client.post("/collections", json=sample_collection_data)
        collection_id = response.json()["id"]
        
        # Verify collection exists
        get_response = client.get(f"/collections/{collection_id}")
        assert get_response.status_code == 200

        # Delete collection
        delete_response = client.delete(f"/collections/{collection_id}")
        assert delete_response.status_code == 204

        # Ensure prompts previously attached to collection are updated
        remaining_prompts = client.get("/prompts").json()["prompts"]
        for prompt in remaining_prompts:
            if prompt["collection_id"] == collection_id:
                assert prompt["collection_id"] is None

        # Verify collection no longer exists
        get_response_after_delete = client.get(f"/collections/{collection_id}")
        assert get_response_after_delete.status_code == 404