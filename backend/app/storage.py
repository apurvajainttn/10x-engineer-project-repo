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

from typing import Dict, List, Optional, Type, Union
from app.models import Prompt, Collection
from collections import defaultdict


class Storage:
    def __init__(self) -> None:
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

    # ============== Private Helper Methods ==============

    def _store_item(self, storage: Dict[str, Union[Prompt, Collection]], item: Union[Prompt, Collection]) -> Union[Prompt, Collection]:
        """
        Stores an item in the specified storage dictionary.

        Args:
            storage (Dict[str, Union[Prompt, Collection]]): The storage dictionary where the item will be stored.
            item (Union[Prompt, Collection]): The item to be added to the storage.

        Returns:
            Union[Prompt, Collection]: The item that was added to the storage.

        Example:
            storage = Storage()
            new_prompt = Prompt(id='abc', content='Hello World')
            storage._store_item(storage._prompts, new_prompt)
        """
        storage[item.id] = item
        return item

    def _retrieve_item_by_id(self, storage: Dict[str, Union[Prompt, Collection]], item_id: str) -> Optional[Union[Prompt, Collection]]:
        """
        Retrieves an item by its ID from the specified storage dictionary.

        Args:
            storage (Dict[str, Union[Prompt, Collection]]): The storage dictionary to search from.
            item_id (str): The unique identifier of the item to retrieve.

        Returns:
            Optional[Union[Prompt, Collection]]: The item retrieved if found, otherwise None.

        Example:
            storage = Storage()
            prompt = storage._retrieve_item_by_id(storage._prompts, 'prompt_id_123')
        """
        return storage.get(item_id)

    def _retrieve_all_items(self, storage: Dict[str, Union[Prompt, Collection]]) -> List[Union[Prompt, Collection]]:
        """
        Retrieves all items from the specified storage dictionary.

        Args:
            storage (Dict[str, Union[Prompt, Collection]]): The storage dictionary containing items.

        Returns:
            List[Union[Prompt, Collection]]: A list of all items in the storage.

        Example:
            storage = Storage()
            prompts = storage._retrieve_all_items(storage._prompts)
        """
        return list(storage.values())

    def _remove_item_by_id(self, storage: Dict[str, Union[Prompt, Collection]], item_id: str) -> bool:
        """
        Removes an item by its ID from the specified storage dictionary.

        Args:
            storage (Dict[str, Union[Prompt, Collection]]): The storage dictionary from which the item will be removed.
            item_id (str): The unique identifier of the item to be removed.

        Returns:
            bool: True if the item was successfully removed, False if it was not found.

        Example:
            storage = Storage()
            result = storage._remove_item_by_id(storage._prompts, "1234")
        """
        if item_id in storage:
            del storage[item_id]
            return True
        return False
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """
        Creates and stores a new prompt in the storage.

        Args:
            prompt (Prompt): The prompt to be added to the storage.

        Returns:
            Prompt: The prompt that was added to the storage.

        Example:
            storage = Storage()
            new_prompt = Prompt(id='abc', content='Hello World')
            storage.create_prompt(new_prompt)
        """
        return self._store_item(self._prompts, prompt)
    
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
        return self._retrieve_item_by_id(self._prompts, prompt_id)
    
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
        return self._retrieve_all_items(self._prompts)
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """
        Updates an existing prompt in the storage.

        Args:
            prompt_id (str): The unique identifier of the prompt to be updated.
            prompt (Prompt): The new prompt data to replace the existing entry.

        Returns:
            Optional[Prompt]: The updated prompt if the update was successful, otherwise None.

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

        Example:
            storage = Storage()
            result = storage.delete_prompt("1234")
            if result:
                print("Prompt deleted successfully.")
            else:
                print("Prompt not found.")
        """
        return self._remove_item_by_id(self._prompts, prompt_id)
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """
        Adds a new collection to the storage.

        Args:
            collection (Collection): The collection object that needs to be added to the storage.
        
        Returns:
            Collection: The collection object that was added to the storage.
    
        Example usage:
            collection = Collection(id='123', ...)
            storage.create_collection(collection)
        """
        return self._store_item(self._collections, collection)
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """
        Retrieves a collection by its ID.

        Args:
            collection_id (str): The unique identifier of the collection to retrieve.

        Returns:
            Optional[Collection]: The collection object if found, otherwise None.
        
        Example:
            storage = Storage()
            collection = storage.get_collection("12345")
            if collection:
                print(f"Collection Found: {collection.name}")
            else:
                print("Collection not found.")
        """
        return self._retrieve_item_by_id(self._collections, collection_id)
    
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
        return self._retrieve_all_items(self._collections)
    
    def delete_collection(self, collection_id: str) -> bool:
        """
        Deletes a collection from storage.

        This method removes the specified collection from the internal storage
        if it exists. Additionally, it clears the collection ID from any associated prompts.

        Args:
            collection_id (str): The unique identifier of the collection to be deleted.

        Returns:
            bool: True if the collection was successfully deleted, False otherwise.

        Example:
            storage = Storage()
            collection_id = 'abc123'
            if storage.delete_collection(collection_id):
                print(f"Collection {collection_id} deleted successfully.")
            else:
                print(f"Collection {collection_id} not found.")
        """
        result = self._remove_item_by_id(self._collections, collection_id)
        if result:
            self.dissociate_prompts_from_collection(collection_id)
        return result
    
    def retrieve_prompts_by_collection_id(self, collection_id: str) -> List[Prompt]:
        """
        Retrieve prompts associated with a specific collection ID.

        Args:
            collection_id (str): The ID of the collection to filter prompts.

        Returns:
            List[Prompt]: A list of Prompt objects that belong to the specified collection.

        Example:
            storage = Storage()
            prompts = storage.get_prompts_by_collection('collection_123')
            for prompt in prompts:
                print(prompt)

        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Tags Operations ==============
    
    def _count_tags_usage(self) -> Dict[str, int]:
        """
        Count the usage of each tag across all prompts.

        Returns:
            Dict[str, int]: A dictionary where keys are tag names and values are their respective usage count.
        """
        tag_counter = defaultdict(int)
        for prompt in self._prompts.values():
            for tag in prompt.tags:
                tag_counter[tag] += 1
        return tag_counter
    
    def get_all_tags(self) -> List[Dict[str, int]]:
        """
        Retrieve all tags used across prompts along with their usage count.

        Returns:
            List[Dict[str, int]]: A list where each entry is a dictionary containing tag and its count.

        Example:
            storage.get_all_tags()
        """
        tag_counter = self._count_tags_usage()
        return [{"name": tag, "prompt_count": count} for tag, count in tag_counter.items()]

    def delete_tag(self, tag_name: str) -> bool:
        """
        Delete a tag from all prompts and storage.

        Returns:
            bool: True if the tag was found and deleted, False otherwise.

        Example:
            storage.delete_tag("example-tag")
        """
        found = False
        for prompt in self._prompts.values():
            if tag_name in prompt.tags:
                prompt.tags.remove(tag_name)
                found = True
        return found
    
    # ============== Utility ==============
    
    def clear(self) -> None:
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

    def dissociate_prompts_from_collection(self, collection_id: str) -> None:
        """
        Clears the specified collection ID from all prompts.

        This method iterates over all stored prompts and sets the `collection_id` to `None` 
        for any prompt that currently has the specified `collection_id`. 

        Args:
            collection_id (str): The ID of the collection to be cleared from the prompts.

        Returns:
            None

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


