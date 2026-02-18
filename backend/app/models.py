"""
Pydantic models for PromptLab

This module includes models for prompts, collections, and response structures 
designed to be used within the PromptLab application. Each model is defined 
using Pydantic's BaseModel to provide data validation and serialization.

Functions:
    generate_id(): Generates a unique identifier using UUID4.
    get_current_time(): Retrieves the current UTC time.

Classes:
    PromptBase: Base model for prompts.
    PromptCreate: Model for creating prompts.
    PromptUpdate: Model for updating prompts.
    PromptPatch: Model for partial prompt updates.
    Prompt: Represents a stored prompt with metadata.
    CollectionBase: Base model for collections.
    CollectionCreate: Model for creating collections.
    Collection: Represents a collection with metadata.
    PromptList: Represents a list of prompts.
    CollectionList: Represents a list of collections.
    HealthResponse: Provides health status and version info.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    """
    Generate a unique identifier as a string using UUID version 4.

    Returns:
        str: A unique identifier string generated using UUID4.

    Example usage:
        >>> unique_id = generate_id()
        >>> print(unique_id)
        'f47ac10b-58cc-4372-a567-0e02b2c3d479'
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """
    Get the current UTC time.

    This function returns the current time in Coordinated Universal Time (UTC).

    Args:
        None

    Returns:
        datetime: The current UTC time.

    Example usage:
        >>> current_time = get_current_time()
        >>> print(current_time)
        datetime.datetime(2023, 10, 5, 12, 0, 0)
    """
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """
    Base model for prompts in the application.

    Attributes:
        title (str): The title of the prompt, required, with a minimum length of 1 and maximum of 200 characters.
        content (str): The main content of the prompt, required with at least 1 character.
        description (Optional[str]): An optional description of the prompt, with a maximum length of 500 characters.
        collection_id (Optional[str]): An optional collection identifier that associates the prompt with a specific collection.

    Example usage:
        ```python
        prompt_data = {
            "title": "Sample Prompt",
            "content": "This is a sample content for the prompt.",
            "description": "A brief description of the prompt.",
            "collection_id": "12345"
        }
        prompt = PromptBase(**prompt_data)
        ```
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class PromptCreate(PromptBase):
    """
    Model for creating a new prompt, extending from PromptBase.

    Inherits all fields from `PromptBase` which include:
    - title (str): The title of the prompt.
    - content (str): The main content of the prompt.
    - description (Optional[str]): A brief description of the prompt.
    - collection_id (Optional[str]): An identifier for associating the prompt with a collection.

    Example usage:
        ```python
        new_prompt = PromptCreate(
            title="New Prompt",
            content="Prompt content details",
            description="Optional description",
            collection_id="collection123"
        )
        ```
    """
    pass


class PromptUpdate(PromptBase):
    """
    Model for updating an existing prompt, extending from PromptBase.

    Inherits all fields from `PromptBase` which include:
    - title (str): The title of the prompt.
    - content (str): The main content of the prompt.
    - description (Optional[str]): A brief description of the prompt.
    - collection_id (Optional[str]): An identifier for associating the prompt with a collection.

    Example usage:
        ```python
        update_prompt = PromptUpdate(
            title="Updated Title",
            content="Updated content details",
            description="Updated description",
            collection_id="updatedCollection123"
        )
        ```
    """
    pass

class PromptPatch(BaseModel):
    """
    Model used for PATCH (partial update) requests.
    All fields are optional, making it suitable for partial updates.

    Attributes:
        title (Optional[str]): The title of the prompt, optional with a minimum length of 1 and maximum of 200 characters.
        content (Optional[str]): The main content of the prompt, optional with at least 1 character.
        description (Optional[str]): An optional description of the prompt, with a maximum length of 500 characters.
        collection_id (Optional[str]): An optional collection identifier that associates the prompt with a specific collection.

    Example usage:
        ```python
        patch_prompt = PromptPatch(
            title="Partial Update Title"
            # Any combination of fields can be provided
        )
        ```
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class Prompt(PromptBase):
    """
    Model representing a stored prompt, extending from PromptBase.

    Attributes:
        id (str): Unique identifier for the prompt, generated using UUID.
        created_at (datetime): The timestamp when the prompt was created, with default as the current UTC time.
        updated_at (datetime): The timestamp when the prompt was last updated, with default as the current UTC time.

    Example usage:
        ```python
        stored_prompt = Prompt(
            title="Stored Prompt",
            content="Content for the stored prompt",
            description="Stored prompt description",
            collection_id="collection456"
        )
        print(stored_prompt.id)
        ```
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """
    Represents the base structure for a Collection.

    Attributes:
        name: The name of the collection. Must be between 1 and 100 characters.
        description: An optional description for the collection. Maximum of 500 characters.

    Example usage:
        collection = CollectionBase(name='Artifacts', description='A collection of ancient artifacts.')
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """
    Represents a request to create a new collection, extending CollectionBase.

    Inherits all attributes from CollectionBase.

    Example usage:
        collection_create = CollectionCreate(name='Artifacts')
    """
    pass


class Collection(CollectionBase):
    """
    Represents a fully-fledged Collection with additional metadata.

    Attributes:
        id: A unique identifier for the collection, generated automatically.
        created_at: The timestamp when the collection was created.

    Inherits all attributes from CollectionBase.

    Example usage:
        collection = Collection(id='123', name='Artifacts', created_at=datetime.now())
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """
    Model representing a list of prompts along with the total count of the prompts.

    Attributes:
        prompts (List[Prompt]): A list containing `Prompt` objects.
        total (int): The total number of prompts.

    Example usage:
        ```python
        prompt_list = PromptList(
            prompts=[Prompt(title="Sample", content="Sample content")],
            total=1
        )
        ```
    """
    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """
    Model representing a list of collections along with the total count of the collections.

    Attributes:
        collections (List[Collection]): A list containing `Collection` objects.
        total (int): The total number of collections.

    Example usage:
        ```python
        collection_list = CollectionList(
            collections=[Collection(name="Sample Collection")],
            total=1
        )
        ```
    """
    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """
    Model providing the health status and version information of the application.

    Attributes:
        status (str): The current status of the application, often displayed as "healthy" or "unhealthy".
        version (str): The version of the application, represented as a string.

    Example usage:
        ```python
        health_response = HealthResponse(status="healthy", version="1.0.0")
        ```
    """
    status: str
    version: str
