import pytest
from pydantic import ValidationError
from app.models import (
    PromptCreate,
    PromptUpdate,
    PromptPatch,
    Prompt,
    CollectionCreate,
    Collection,
    generate_unique_identifier,
    get_current_utc_time,
    HealthResponse
)


def test_prompt_create_model_validation():
    """
    Test the PromptCreate model for validation.

    Ensures that:
    - A valid PromptCreate instance can be created.
    - An invalid title or content raises a ValidationError.

    Raises:
        pytest.raises: If any field is invalid during PromptCreate initialization.
    """
    valid_data = {
        'title': 'Valid Title',
        'content': 'Valid content.',
        'description': 'A description',
        'collection_id': '1234'
    }

    # Model creation should succeed
    prompt = PromptCreate(**valid_data)
    assert prompt.title == 'Valid Title'
    assert prompt.content == 'Valid content.'

    # Invalid title (too short)
    invalid_data = valid_data.copy()
    invalid_data['title'] = ''
    
    with pytest.raises(ValidationError):
        PromptCreate(**invalid_data)

    # Invalid content (too short)
    invalid_data = valid_data.copy()
    invalid_data['content'] = ''

    with pytest.raises(ValidationError):
        PromptCreate(**invalid_data)


def test_prompt_update_model_validation():
    """
    Test the PromptUpdate model for validation compliance.

    Ensures that:
    - Valid PromptUpdate instances respect optional field constraints.
    - Invalid field data raises a ValidationError.

    Raises:
        pytest.raises: If any field does not meet the expected criteria.
    """
    # All fields optional, but still should respect min_length constraints
    valid_data = {
        'title': 'New Title',
        'content': 'Updated Content'
    }
    
    # Model creation should succeed
    prompt_update = PromptUpdate(**valid_data)
    assert prompt_update.title == 'New Title'
    
    # Invalid title (too short)
    invalid_data = {'title': ''}
    with pytest.raises(ValidationError):
        PromptUpdate(**invalid_data)


def test_prompt_patch_model_validation():
    """
    Test the PromptPatch model for partial updates.

    Confirms that:
    - Partial updates with valid fields succeed.
    - Validation correctly identifies invalid fields.

    Raises:
        pytest.raises: For any improperly formatted partial update.
    """
    # Test valid partial update
    patch_data = {'title': 'Partial Title'}
    prompt_patch = PromptPatch(**patch_data)
    assert prompt_patch.title == 'Partial Title'

    # Invalid partial update
    invalid_data = {'title': ''}
    with pytest.raises(ValidationError):
        PromptPatch(**invalid_data)


def test_prompt_default_values():
    """
    Verify default value generation in the Prompt model.

    Ensures that ID and timestamps:
    - Are automatically generated upon Prompt model instantiation.
    - Are not None.
    """
    # Prompt should auto-generate ID and timestamps
    prompt = Prompt(
        title='Title',
        content='Content'
    )

    assert prompt.id is not None
    assert prompt.created_at is not None
    assert prompt.updated_at is not None


def test_collection_create_model_validation():
    """
    Validate the CollectionCreate model's constraints.

    Ensures that:
    - Valid instance creation is successful with appropriate data.
    - ValidationError is raised for invalid names.

    Raises:
        pytest.raises: If collection name does not meet length requirements.
    """
    valid_data = {'name': 'Collection Name', 'description': 'Description'}
    collection = CollectionCreate(**valid_data)
    assert collection.name == 'Collection Name'

    # Invalid name (too short)
    invalid_data = valid_data.copy()
    invalid_data['name'] = ''

    with pytest.raises(ValidationError):
        CollectionCreate(**invalid_data)


def test_collection_default_values():
    """
    Test default value assignments in the Collection model.

    Ensures that:
    - ID and created_at timestamp are populated automatically.
    - These fields are not None when the model is initialized.
    """
    # Collection should auto-generate ID and created_at timestamp
    collection = Collection(
        name='Collection Name'
    )
    
    assert collection.id is not None
    assert collection.created_at is not None


def test_health_response_serialization():
    """
    Test the HealthResponse model's serialization capability.

    Ensures that:
    - Model can be serialized to a dictionary.
    - Serialized data matches expected key values.
    """
    response = HealthResponse(status='healthy', version='1.0.0')

    serialized = response.dict()
    assert serialized['status'] == 'healthy'
    assert serialized['version'] == '1.0.0'