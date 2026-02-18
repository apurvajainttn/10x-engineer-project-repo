"""
In-memory storage for PromptLab.

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.

Classes:
    Storage: A class for handling operations related to prompts and collections within an in-memory storage system.

Functions:
    create_prompt: Adds a new prompt to the storage.
    get_prompt: Retrieves a prompt by its ID.
    get_all_prompts: Retrieves all prompts stored in the system.
    update_prompt: Updates an existing prompt in the storage.
    delete_prompt: Deletes a prompt from storage.
    create_collection: Adds a new collection to the storage.
    get_collection: Retrieves a collection by its ID.
    get_all_collections: Retrieves all collections stored in the system.
    delete_collection: Deletes a collection from storage.
    get_prompts_by_collection: Retrieve prompts associated with a specific collection ID.
    clear: Clears all entries in the storage.
    clear_collection_id_from_prompts: Clears the specified collection ID from all prompts.

A global instance of the Storage class, 'storage', is used to store prompts and collections in memory.
This instance is used throughout the application to manage and retrieve prompts and collections without persisting
data to a permanent datastore. It's suitable for development and testing environments.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


class Storage:
    def __init__(self):
        """
        Initializes an instance of the Storage class.

        This constructor sets up the internal storage dictionaries for prompts and collections.

        Attributes:
            self._prompts (Dict[str, Prompt]): A dictionary to store prompts, keyed by their ID.
            self._collections (Dict[str, Collection]): A dictionary to store collections, keyed by their ID.

        Raises:
            None

        Example:
            storage_instance = Storage()
        """
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """
        Creates and stores a new prompt in the storage.

        Args:
            prompt (Prompt): The prompt to be added to the storage.

        Returns:
            Prompt: The prompt that was added to the storage.

        Raises:
            KeyError: If a prompt with the same ID already exists in the storage.

        Example:
            storage = Storage()
            new_prompt = Prompt(id='abc', content='Hello World')
            storage.create_prompt(new_prompt)
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """
        Retrieves a prompt by its ID from the storage.

        Args:
            prompt_id (str): The unique identifier of the prompt to retrieve.

        Returns:
            Optional[Prompt]: The prompt associated with the given ID if found, otherwise None.

        Raises:
            None

        Example:
            storage = Storage()
            prompt = storage.get_prompt('prompt_id_123')
            if prompt:
                print("Prompt found:", prompt.content)
            else:
                print("Prompt not found.")
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """
        Retrieve all prompts from the storage.

        This method returns a list of all `Prompt` objects stored in the system.

        Args:
            None

        Returns:
            List[Prompt]: A list containing all stored `Prompt` objects.

        Raises:
            No exceptions are raised by this method.

        Example:
            prompts = storage_instance.get_all_prompts()
            for prompt in prompts:
                print(prompt)
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """
        Updates an existing prompt in the storage.

        Args:
            prompt_id (str): The unique identifier of the prompt to be updated.
            prompt (Prompt): The new prompt data to replace the existing entry.

        Returns:
            Optional[Prompt]: The updated prompt if the update was successful, otherwise None.

        Raises:
            KeyError: If the prompt_id does not exist in the storage.

        Example:
            storage = Storage()
            updated_prompt = storage.update_prompt("prompt123", new_prompt)
            if updated_prompt:
                print("Prompt updated successfully.")
            else:
                print("Prompt ID not found.")
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """
        Deletes a prompt from storage by its unique identifier.

        Args:
            prompt_id (str): The unique identifier of the prompt to be deleted.

        Returns:
            bool: True if the prompt was successfully deleted, False if the prompt was not found.

        Raises:
            KeyError: If an attempt is made to delete a prompt that does not exist in the storage.

        Example:
            storage = Storage()
            result = storage.delete_prompt("1234")
            if result:
                print("Prompt deleted successfully.")
            else:
                print("Prompt not found.")
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """
        Adds a new collection to the storage.

        Args:
            collection (Collection): The collection object that needs to be added to the storage.
        
        Returns:
            Collection: The collection object that was added to the storage.

        Raises:
            KeyError: If a collection with the same id already exists.
    
        Example usage:
            collection = Collection(id='123', ...)
            storage.create_collection(collection)
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """
        Retrieves a collection by its ID.

        Args:
            collection_id (str): The unique identifier of the collection to retrieve.

        Returns:
            Optional[Collection]: The collection object if found, otherwise None.

        Raises:
            KeyError: If the collection_id is not found in the collections dictionary.
        
        Example:
            storage = Storage()
            collection = storage.get_collection("12345")
            if collection:
                print(f"Collection Found: {collection.name}")
            else:
                print("Collection not found.")
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """
        Retrieves all collections stored in the system.

        This function returns a list containing all the collection
        objects that are currently stored in the system.

        Args:
            None

        Returns:
            List[Collection]: A list of Collection objects currently stored.

        Raises:
            ExceptionType: Description of the exception (if any are applicable).

        Example:
            collections = storage_instance.get_all_collections()
            for collection in collections:
                print(collection.name)
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """
        Deletes a collection from storage.

        This method removes the specified collection from the internal storage
        if it exists. Additionally, it clears the collection ID from any associated prompts.

        Args:
            collection_id (str): The unique identifier of the collection to be deleted.

        Returns:
            bool: True if the collection was successfully deleted, False otherwise.

        Raises:
            KeyError: If the collection_id is not present in the storage.

        Example:
            storage = Storage()
            collection_id = 'abc123'
            if storage.delete_collection(collection_id):
                print(f"Collection {collection_id} deleted successfully.")
            else:
                print(f"Collection {collection_id} not found.")
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            # Clear collection_id from prompts associated with this collection
            self.clear_collection_id_from_prompts(collection_id)
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """
        Retrieve prompts associated with a specific collection ID.

        Args:
            collection_id (str): The ID of the collection to filter prompts.

        Returns:
            List[Prompt]: A list of Prompt objects that belong to the specified collection.

        Raises:
            KeyError: If the collection with the specified ID does not exist.

        Example:
            storage = Storage()
            prompts = storage.get_prompts_by_collection('collection_123')
            for prompt in prompts:
                print(prompt)

        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        """
        Clear all entries in the storage.

        This method removes all stored prompts and collections, resetting the storage
        to its initial empty state.

        Args:
            None

        Returns:
            None

        Raises:
            No exceptions are raised by this method.

        Example:
            storage = Storage()
            storage.add_prompt("What is your name?")
            storage.clear()
            # Now storage is empty: storage._prompts and storage._collections are empty.
        """
        self._prompts.clear()
        self._collections.clear()

    def clear_collection_id_from_prompts(self, collection_id: str):
        """
        Clears the specified collection ID from all prompts.

        This method iterates over all stored prompts and sets the `collection_id` to `None` 
        for any prompt that currently has the specified `collection_id`. 

        Args:
            collection_id (str): The ID of the collection to be cleared from the prompts.

        Returns:
            None

        Raises:
            KeyError: If a prompt does not have a `collection_id` attribute.

        Example:
            storage = Storage()
            storage.clear_collection_id_from_prompts('1234')
        """
        for prompt in self._prompts.values():
            if prompt.collection_id == collection_id:
                prompt.collection_id = None


"""
A global instance of the Storage class, used to store prompts and collections in memory.

This instance is utilized in the application to manage and retrieve prompts and collections without persisting
data to a permanent datastore. It's suitable for development and testing environments.

Attributes:
    None

Example:
    # Access the global storage instance to create a new prompt
    global storage
    new_prompt = Prompt(id='123', content='Example content')
    storage.create_prompt(new_prompt)
"""
storage = Storage()


