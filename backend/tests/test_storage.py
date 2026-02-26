import pytest
from app.storage import Storage
from app.models import Prompt, Collection

@pytest.fixture
def storage():
    """Fixture for setting up a Storage instance for testing.

    Returns:
        Storage: An instance of the Storage class for use in testing.
    """
    return Storage()


def test_create_prompt(storage):
    """Test creating a prompt and verify it can be retrieved.

    Args:
        storage (Storage): The storage instance with which to test prompt creation.

    Asserts:
        The result of the creation is the same as the prompt object.
        The prompt can be retrieved correctly from storage.
    """
    prompt = Prompt(id="1", title="Title", content="Test Prompt")
    result = storage.create_prompt(prompt)
    assert result == prompt
    assert storage.get_prompt(prompt.id) == prompt


def test_get_prompt(storage):
    """Test retrieving a prompt by ID and ensure it handles non-existing IDs.

    Args:
        storage (Storage): The storage instance with which to test prompt retrieval.

    Asserts:
        The prompt can be retrieved correctly from storage using its ID.
        A non-existing ID returns None when retrieved.
    """
    prompt = Prompt(id="2", title="Title 2", content="Another Test")
    storage.create_prompt(prompt)
    assert storage.get_prompt(prompt.id) == prompt
    assert storage.get_prompt("non_existing_id") is None


def test_update_non_existent_prompt(storage):
    """Test attempting to update a non-existent prompt.

    Args:
        storage (Storage): The storage instance with which to test updating a prompt.

    Asserts:
        Updating a non-existent prompt returns None.
    """
    # Attempt to update a non-existent prompt
    non_existent_prompt = Prompt(id="nonexistent", title="Title 3", content="Nothing")
    assert storage.update_prompt("nonexistent", non_existent_prompt) is None


def test_delete_non_existent_prompt(storage):
    """Test attempting to delete a non-existent prompt.

    Args:
        storage (Storage): The storage instance with which to test deleting a prompt.

    Asserts:
        Deleting a non-existent prompt returns False.
    """
    # Attempt to delete a non-existent prompt
    assert storage.delete_prompt("nonexistent") is False


def test_create_collection(storage):
    """Test creating a collection and verify it can be retrieved.

    Args:
        storage (Storage): The storage instance with which to test collection creation.

    Asserts:
        The result of the creation is the same as the collection object.
        The collection can be retrieved correctly from storage.
    """
    collection = Collection(id="1", name="Test Collection")
    result = storage.create_collection(collection)
    assert result == collection
    assert storage.get_collection(collection.id) == collection


def test_get_collection(storage):
    """Test retrieving a collection by ID and ensure it handles non-existing IDs.

    Args:
        storage (Storage): The storage instance with which to test collection retrieval.

    Asserts:
        The collection can be retrieved correctly from storage using its ID.
        A non-existing ID returns None when retrieved.
    """
    collection = Collection(id="2", name="Another Test Collection")
    storage.create_collection(collection)
    assert storage.get_collection(collection.id) == collection
    assert storage.get_collection("non_existing_id") is None


def test_delete_non_existent_collection(storage):
    """Test attempting to delete a non-existent collection.

    Args:
        storage (Storage): The storage instance with which to test deleting a collection.

    Asserts:
        Deleting a non-existent collection returns False.
    """
    # Attempt to delete a non-existent collection
    assert storage.delete_collection("nonexistent") is False


def test_get_prompts_by_collection(storage):
    """Test retrieving prompts by collection ID and verify correct prompts are returned.

    Args:
        storage (Storage): The storage instance with which to test retrieving prompts by collection.

    Asserts:
        Correct number of prompts are retrieved for a given collection ID.
        Prompts belonging to the collection are retrieved.
        Prompts not belonging to the collection are not retrieved.
    """
    collection = Collection(id="collect1", name="Test Collection")
    prompt1 = Prompt(id="p1", title="Title 4", content="Prompt 1", collection_id="collect1")
    prompt2 = Prompt(id="p2", title="Title 5", content="Prompt 2", collection_id="collect1")
    prompt3 = Prompt(id="p3", title="Title 6", content="Prompt 3", collection_id="collect2")

    storage.create_collection(collection)
    storage.create_prompt(prompt1)
    storage.create_prompt(prompt2)
    storage.create_prompt(prompt3)

    collection_prompts = storage.get_prompts_by_collection(collection.id)
    assert len(collection_prompts) == 2
    assert prompt1 in collection_prompts
    assert prompt2 in collection_prompts
    assert prompt3 not in collection_prompts


def test_clear(storage):
    """Test clearing all data in storage.

    Args:
        storage (Storage): The storage instance with which to test clearing data.

    Asserts:
        After clearing, all prompts and collections are removed from storage.
    """
    storage.create_prompt(Prompt(id="c1", title="Title 7", content="Clear Test"))
    storage.create_collection(Collection(id="c2", name="Clear Collection"))
    storage.clear()
    assert storage.get_all_prompts() == []
    assert storage.get_all_collections() == []


def test_clear_collection_id_from_prompts(storage):
    """Test clearing collection ID from prompts.

    Args:
        storage (Storage): The storage instance with which to test clearing collection IDs.

    Asserts:
        After clearing, prompts' collection ID fields are set to None.
    """
    prompt1 = Prompt(id="cp1", title="Title 8", content="Prompt 1", collection_id="clear_id")
    prompt2 = Prompt(id="cp2", title="Title 9", content="Prompt 2", collection_id="clear_id")
    storage.create_prompt(prompt1)
    storage.create_prompt(prompt2)

    storage.clear_collection_id_from_prompts("clear_id")
    assert storage.get_prompt("cp1").collection_id is None
    assert storage.get_prompt("cp2").collection_id is None


def test_data_persistence_within_session(storage):
    """Test data persistence within a session and verify it is cleared properly.

    Args:
        storage (Storage): The storage instance with which to test session data persistence.

    Asserts:
        All created prompts and collections persist within the session.
        Data is removed after clearing storage.
    """
    # Create prompts
    prompt1 = Prompt(id="persist1", title="Persist Title 1", content="Persist Content 1")
    prompt2 = Prompt(id="persist2", title="Persist Title 2", content="Persist Content 2")

    storage.create_prompt(prompt1)
    storage.create_prompt(prompt2)

    # Create collections
    collection1 = Collection(id="coll1", name="Persist Collection 1")
    collection2 = Collection(id="coll2", name="Persist Collection 2")

    storage.create_collection(collection1)
    storage.create_collection(collection2)

    # Assert data persistence
    assert len(storage.get_all_prompts()) == 2
    assert storage.get_prompt("persist1").title == "Persist Title 1"
    assert storage.get_prompt("persist2").title == "Persist Title 2"

    assert len(storage.get_all_collections()) == 2
    assert storage.get_collection("coll1").name == "Persist Collection 1"
    assert storage.get_collection("coll2").name == "Persist Collection 2"

    # Clear storage and ensure data is removed
    storage.clear()
    assert len(storage.get_all_prompts()) == 0
    assert len(storage.get_all_collections()) == 0


def test_edge_cases(storage):
    """Test edge cases such as using empty string IDs in storage.

    Args:
        storage (Storage): The storage instance with which to test edge cases.

    Asserts:
        Prompts and collections can still be retrieved correctly using empty string IDs.
    """
    # Test with empty string IDs
    empty_id_prompt = Prompt(id="", title="Empty ID", content="Empty ID Content")
    storage.create_prompt(empty_id_prompt)
    assert storage.get_prompt("") == empty_id_prompt

    empty_id_collection = Collection(id="", name="Empty ID Collection")
    storage.create_collection(empty_id_collection)
    assert storage.get_collection("") == empty_id_collection

def test_get_all_tags(storage):
     # Arrange
     prompt1 = Prompt(id='3', title='Prompt 1', content='Content 1', tags=['tag1', 'tag2'])
     prompt2 = Prompt(id='4', title='Prompt 2', content='Content 2', tags=['tag2', 'tag3'])

     storage.create_prompt(prompt1)
     storage.create_prompt(prompt2)

     # Act
     tags = storage.get_all_tags()

     # Assert
     expected_tags = [{'name': 'tag1', 'prompt_count': 1}, {'name': 'tag2', 'prompt_count': 2}, {'name': 'tag3', 'prompt_count': 1}]
     assert all(tag in tags for tag in expected_tags)


def test_delete_tag(storage):
     # Arrange
     prompt = Prompt(id='5', title='Prompt Tag', content='Content Tag', tags=['delete-me'])
     storage.create_prompt(prompt)

     # Act
     tag_deleted = storage.delete_tag('delete-me')

     # Assert
     assert tag_deleted
     updated_prompt = storage.get_prompt('5')
     assert 'delete-me' not in updated_prompt.tags


