"""
FastAPI Application for PromptLab API

This module sets up the FastAPI application, routing, and middleware configuration
for handling operations related to prompts and collections in PromptLab.

API Endpoints:
- Health Check: Provides a health status of the API service.
- Prompts: CRUD operations for managing prompt objects, including listing, fetching,
  creating, updating, and deleting prompts.
- Collections: CRUD operations for managing collection objects linked with prompts.

Middleware:
- CORS: Configured to allow cross-origin requests from any origin, with credentials,
  allowing all HTTP methods and headers.

Modules:
- FastAPI: The core framework used for building and handling API requests.
- CORSMiddleware: Middleware for enabling CORS.
- Typing: Used for type hinting optional parameters.
- Models and Utilities Modules: Imported from the app package for handling prompt
  and collection logic, storage interactions, and utility functions such as sorting 
  and searching prompts.

Usage:
To start the API server, run the FastAPI application to expose the defined endpoints
and interact with the prompt and collection management functionalities programmatically.

Example:
  To start the server:
      $ uvicorn app.api:app --reload

  To test the health check endpoint:
      $ curl http://localhost:8000/health
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate, PromptPatch,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    get_current_time
)
from app.storage import storage
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts
from app import __version__

"""
Initializes the FastAPI application with configuration details and middleware.

The FastAPI application is set up with the title, description, and version
information. This is the main entry point for the API routes and includes
middleware for CORS which allows cross-origin requests.
"""
app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

"""
CORS Configuration:
    - allow_origins: Specifies which origins are permitted to access the API.
    - allow_credentials: Allows cookies to be included in the requests.
    - allow_methods: Lists HTTP methods that are permitted.
    - allow_headers: Lists the headers that can be used in the requests.
"""
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Performs a health check for the API service.

    This endpoint returns the status and version of the API to indicate its health status.

    Args:
        None

    Returns:
        HealthResponse: A pydantic model containing the status and version of the API.

    Raises:
        HTTPException: If there is an issue in fetching the API status (not anticipated in current implementation).

    Example:
        To check the health of the service, you can use:

        >>> import requests
        >>> response = requests.get('http://<api-url>/health')
        >>> print(response.json())
        {'status': 'healthy', 'version': '1.0.0'}
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """
    Retrieves a list of prompts optionally filtered by collection and search query.

    Args:
        collection_id (Optional[str]): An optional collection ID to filter the prompts.
        search (Optional[str]): An optional search string to filter prompts by keyword.

    Returns:
        PromptList: A list of prompts sorted by date (newest first) with the total count.

    Raises:
        HTTPException: If there is an issue accessing storage or processing prompts.

    Example:
        >>> import requests
        >>> response = requests.get('http://<api-url>/prompts?collection_id=123&search=my_query')
        >>> print(response.json())
        {'prompts': [...], 'total': 5}
    """
    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    
    # Sort by date (newest first)
    # Note: Issue with the sorting is fixed...
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """
    Retrieve a specific prompt by its ID.

    This endpoint fetches a specific prompt from the storage if it exists. 
    If the prompt does not exist, it raises a 404 HTTPException.

    Args:
        prompt_id (str): The unique identifier of the prompt to retrieve.

    Returns:
        Prompt: A pydantic model of the prompt, if found.

    Raises:
        HTTPException: If no prompt is found with the given ID, a 404 error is raised.

    Example:
        To retrieve a specific prompt by its ID, you can use:

        >>> import requests
        >>> response = requests.get('http://<api-url>/prompts/123')
        >>> print(response.json())
        {'id': '123', 'title': 'Sample Prompt', 'content': '...'}
    """
    # BUG #1: This is fixed now, and this will raise a 404 error if prompt doesn't exist
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """
    Creates a new prompt in the system.

    This endpoint allows you to create a new prompt in the data store. 
    If a `collection_id` is provided in the `prompt_data`, it verifies whether the collection exists.

    Args:
        prompt_data (PromptCreate): The data required to create a prompt. This includes all necessary attributes defined in the `PromptCreate` model.

    Returns:
        Prompt: The newly created prompt object.

    Raises:
        HTTPException: If a `collection_id` is provided and the corresponding collection does not exist, a 400 HTTP exception is raised with the message "Collection not found".

    Example:
        >>> prompt_data = PromptCreate(title="New Prompt", description="This is a new prompt", collection_id=1)
        >>> create_prompt(prompt_data)
    """
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """
    Update an existing prompt by its ID.

    This endpoint updates the details of a specific prompt identified by `prompt_id`.
    It validates the existence of the prompt and its associated collection (if provided)
    before updating the prompt details and setting the updated_at timestamp to the current time.

    Args:
        prompt_id (str): The unique identifier of the prompt to update.
        prompt_data (PromptUpdate): The data for updating the prompt, which includes title,
            content, description, and optionally the associated collection ID.

    Returns:
        Prompt: The updated prompt object.

    Raises:
        HTTPException: If the prompt does not exist (404) or if the provided collection
            does not exist (400).

    Example:
        >>> update_prompt("prompt123", PromptUpdate(title="New Title", content="New Content"))
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # BUG #2 Fixed: We're now updating the updated_at timestamp!
    # The updated prompt now keeps the latest and current time
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_prompt=Prompt(
            id=existing.id,
            title=prompt_data.title,
            content=prompt_data.content,
            description=prompt_data.description,
            collection_id=prompt_data.collection_id,
            created_at=existing.created_at,
            updated_at=get_current_time()  # Fix: Update to current time
        )
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


# ============== Prompt Endpoints ==============

# NOTE: PATCH endpoint implemented.

@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptPatch):
    """
    Update an existing prompt with new data.

    This function updates the fields of an existing prompt based on the 
    provided data. Only fields explicitly set in `prompt_data` will be 
    updated, leaving other fields unchanged. The function checks the 
    existence of both the prompt and any new collection it belongs to 
    before applying the update.

    Args:
        prompt_id (str): The unique identifier of the prompt to update.
        prompt_data (PromptPatch): An object containing the fields to update.

    Returns:
        Prompt: The updated prompt instance.

    Raises:
        HTTPException: If the prompt does not exist (404) or no fields are 
        provided for update (400), or if the updated collection is not found 
        (400).

    Example:
        >>> patch_data = PromptPatch(title="New Title")
        >>> patch_prompt("1234", patch_data)

    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Extract the provided fields to update
    update_prompt_data = prompt_data.model_dump(exclude_unset=True)
    if not update_prompt_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    # Validate collection of the prompt if being updated
    if "collection_id" in update_prompt_data and update_prompt_data["collection_id"]:
        collection = storage.get_collection(update_prompt_data["collection_id"])
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
        # Merge existing prompt data with updated prompt data
    updated_prompt = Prompt(
        id=existing.id,
        title=update_prompt_data.get("title", existing.title),
        content=update_prompt_data.get("content", existing.content),
        description=update_prompt_data.get("description", existing.description),
        collection_id=update_prompt_data.get("collection_id", existing.collection_id),
        created_at=existing.created_at,
        updated_at=get_current_time(),
    )

    return storage.update_prompt(prompt_id, updated_prompt)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """
    Delete a prompt by its unique identifier.

    Args:
        prompt_id (str): The unique identifier of the prompt to be deleted.

    Returns:
        None: This function does not return a value but raises exceptions in cases of failure.

    Raises:
        HTTPException: If the prompt with the given prompt_id is not found, it raises a 404 HTTPException.

    Example usage:
        - Delete a prompt with a known ID:
            delete_prompt("12345")

        - Handle case where prompt might not exist:
            try:
                delete_prompt("67890")
            except HTTPException as e:
                print("Prompt not found", e)
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """
    List all collections.

    Fetches and returns a list of all collections stored in the system along with the total count.

    Args:
        None

    Returns:
        CollectionList: An object containing a list of collections and the total number of collections.

    Raises:
        HTTPException: If there is an error retrieving collections from storage.

    Example:
        >>> response = client.get("/collections")
        >>> assert response.status_code == 200
        >>> assert "total" in response.json()
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """
    Retrieve a collection by its unique identifier.

    Args:
        collection_id (str): The unique identifier of the collection to retrieve.

    Returns:
        Collection: The collection corresponding to the given identifier.

    Raises:
        HTTPException: If the collection is not found, raises a 404 HTTP status code.

    Example:
        ```
        try:
            collection = get_collection("12345")
        except HTTPException as e:
            print(e.detail)
        ```
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """
    Create a new collection in the system.

    This endpoint allows the creation of a new collection with the provided data.

    Args:
        collection_data (CollectionCreate): A pydantic model containing the data needed to create a collection.

    Returns:
        Collection: The newly created collection object.

    Raises:
        HTTPException: An error indicating storage issues or validation failures may be raised, though not anticipated in the current implementation.

    Example:
        >>> collection_data = CollectionCreate(name="New Collection", description="A test collection")
        >>> create_collection(collection_data)
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """
    Deletes a collection and clears its associated prompts.

    This function deletes a collection specified by the collection_id. 
    All prompts associated with this `collection_id` will have their `collection_id` 
    set to `None` once the collection is deleted.

    Args:
        collection_id (str): The unique identifier of the collection to be deleted.

    Returns:
        None: This function returns nothing on successful deletion.

    Raises:
        HTTPException: An exception is raised with a 404 status code if the collection
                       does not exist.

    Example usage:
        >>> delete_collection('collection123')
    """
    # BUG #4 Fixed: We now handle the prompts while delete the collection!
    # Prompts with this collection_id will now have collection_id None once collection is deleted
    
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")
    
    return None

