"""
Utility functions for PromptLab

This module provides several utility functions to handle operations on `Prompt` objects.
These operations include sorting, filtering, searching, validating content, and extracting
template variables. The utilities are designed to support efficient management and utilization
of prompts in the PromptLab application.

Main functionalities:
- Sort prompts by their creation date
- Filter prompts by a specified collection ID
- Search through prompts using query strings
- Validate the content of a prompt
- Extract template variables from prompt content

The functions within this module interact with the `Prompt` model and assume that each
`Prompt` object has specific attributes like `created_at`, `collection_id`, `title`, and
`description`.

Usage examples for each function can be found in their respective docstrings.
"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """
    Sort prompts by creation date.

    This function sorts a list of `Prompt` objects by their `created_at` date field.

    Args:
        prompts (List[Prompt]): A list of `Prompt` objects to be sorted.
        descending (bool): A boolean flag indicating whether the prompts should be sorted
            in descending order. Defaults to True.

    Returns:
        List[Prompt]: A list of `Prompt` objects sorted by creation date.

    Raises:
        ValueError: If any element in `prompts` does not have a `created_at` attribute.

    Example:
        >>> prompts = [Prompt(created_at=datetime(2023, 10, 1)), Prompt(created_at=datetime(2023, 9, 15))]
        >>> sorted_prompts = sort_prompts_by_date(prompts)
        >>> # sorted_prompts will sort dates in descending order by default.
    """
    # Fixed: Bug #3 has been resolved. The prompts are now correctly sorted in
    # descending order by default (newest first) as per the `descending`
    # parameter passed to the `sorted()` function.
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """
    Filters a list of prompts by a specified collection ID.

    This function iterates through the provided list of prompts and returns a
    new list containing only the prompts that belong to the specified collection.

    Args:
        prompts (List[Prompt]): A list of Prompt objects to filter.
        collection_id (str): The ID of the collection used for filtering prompts.

    Returns:
        List[Prompt]: A list of Prompt objects that belong to the specified collection ID.

    Raises:
        None

    Example:
        >>> prompts = [Prompt(collection_id='123', ...), Prompt(collection_id='456', ...)]
        >>> filtered_prompts = filter_prompts_by_collection(prompts, '123')
        >>> print(filtered_prompts)
        [<Prompt object at 0x...>]
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """
    Search for prompts in a list that match a given query.

    This function searches through a list of Prompt objects and returns those
    whose title or description contains the specified query string.

    Args:
        prompts (List[Prompt]): A list of Prompt objects to search through.
        query (str): The string query to search for within the titles and descriptions
            of the Prompt objects.

    Returns:
        List[Prompt]: A list of Prompt objects where the title or description 
        contains the query string.

    Raises:
        AttributeError: If a Prompt object does not have a title or description attribute.

    Example:
        >>> prompts = [Prompt(title="Hello World", description="Example description"),
                       Prompt(title="Another Title", description="Another example")]
        >>> search_prompts(prompts, "hello")
        [Prompt(title="Hello World", description="Example description")]
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """
    Check if prompt content is valid.

    A valid prompt should:
    - Not be empty
    - Not be just whitespace
    - Be at least 10 characters

    Args:
        content (str): The prompt content to validate.

    Returns:
        bool: True if the prompt content is valid, False otherwise.

    Raises:
        None

    Examples:
        >>> validate_prompt_content("   ")
        False
        >>> validate_prompt_content("Valid prompt content")
        True
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """
    Extract template variables from prompt content.

    This function searches through the given `content` string to find all occurrences
    of template variables, which are denoted by double curly braces (e.g., {{variable_name}}),
    and returns a list of these variable names.

    Args:
        content (str): The string content from which to extract template variables.

    Returns:
        List[str]: A list of strings, each representing a variable name found within
        the given content.

    Raises:
        None: This function does not explicitly raise any exceptions.

    Example usage:
        >>> extract_variables("Hello, {{name}}! Your account number is {{account_number}}.")
        ['name', 'account_number']
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
