import pytest
from app.storage import Storage
from app.models import Prompt, Collection

@pytest.fixture
def storage():
    return Storage()


def test_create_prompt(storage):
    prompt = Prompt(id="1", title="Title", content="Test Prompt")
    result = storage.create_prompt(prompt)
    assert result == prompt
    assert storage.get_prompt(prompt.id) == prompt


def test_get_prompt(storage):
    prompt = Prompt(id="2", title="Title 2", content="Another Test")
    storage.create_prompt(prompt)
    assert storage.get_prompt(prompt.id) == prompt
    assert storage.get_prompt("non_existing_id") is None


def test_update_non_existent_prompt(storage):
    # Attempt to update a non-existent prompt
    non_existent_prompt = Prompt(id="nonexistent", title="Title 3", content="Nothing")
    assert storage.update_prompt("nonexistent", non_existent_prompt) is None


def test_delete_non_existent_prompt(storage):
    # Attempt to delete a non-existent prompt
    assert storage.delete_prompt("nonexistent") is False


def test_create_collection(storage):
    collection = Collection(id="1", name="Test Collection")
    result = storage.create_collection(collection)
    assert result == collection
    assert storage.get_collection(collection.id) == collection


def test_get_collection(storage):
    collection = Collection(id="2", name="Another Test Collection")
    storage.create_collection(collection)
    assert storage.get_collection(collection.id) == collection
    assert storage.get_collection("non_existing_id") is None


def test_delete_non_existent_collection(storage):
    # Attempt to delete a non-existent collection
    assert storage.delete_collection("nonexistent") is False


def test_get_prompts_by_collection(storage):
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
    storage.create_prompt(Prompt(id="c1", title="Title 7", content="Clear Test"))
    storage.create_collection(Collection(id="c2", name="Clear Collection"))
    storage.clear()
    assert storage.get_all_prompts() == []
    assert storage.get_all_collections() == []


def test_clear_collection_id_from_prompts(storage):
    prompt1 = Prompt(id="cp1", title="Title 8", content="Prompt 1", collection_id="clear_id")
    prompt2 = Prompt(id="cp2", title="Title 9", content="Prompt 2", collection_id="clear_id")
    storage.create_prompt(prompt1)
    storage.create_prompt(prompt2)

    storage.clear_collection_id_from_prompts("clear_id")
    assert storage.get_prompt("cp1").collection_id is None
    assert storage.get_prompt("cp2").collection_id is None


def test_data_persistence_within_session(storage):
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
    # Test with empty string IDs
    empty_id_prompt = Prompt(id="", title="Empty ID", content="Empty ID Content")
    storage.create_prompt(empty_id_prompt)
    assert storage.get_prompt("") == empty_id_prompt

    empty_id_collection = Collection(id="", name="Empty ID Collection")
    storage.create_collection(empty_id_collection)
    assert storage.get_collection("") == empty_id_collection


