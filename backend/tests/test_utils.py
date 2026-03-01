from datetime import datetime
from app.utils import (
    sort_prompts_by_date, filter_prompts_by_collection, search_prompts,
    validate_prompt_content, extract_variables
)
from app.models import Prompt

# Helper function to create a Prompt
def create_prompt(created_at=None, collection_id='default', title='Default Title', description='Default Description', content='Default Content'):
    return Prompt(
        created_at=created_at or datetime.now(),
        collection_id=collection_id,
        title=title,
        description=description,
        content=content
    )

def test_sort_prompts_by_date():
    """
    Test sorting of prompts by creation date.

    Ensures that the `sort_prompts_by_date` function correctly sorts
    prompts by descending order of their creation date.
    """
    prompts = [
        create_prompt(created_at=datetime(2023, 10, 1)),
        create_prompt(created_at=datetime(2023, 10, 5)),
        create_prompt(created_at=datetime(2023, 9, 15))
    ]
    sorted_prompts = sort_prompts_by_date(prompts)
    assert sorted_prompts[0].created_at == datetime(2023, 10, 5)
    assert sorted_prompts[1].created_at == datetime(2023, 10, 1)
    assert sorted_prompts[2].created_at == datetime(2023, 9, 15)

def test_filter_prompts_by_collection():
    """
    Test filtering of prompts by collection ID.

    Validates that only prompts with the specified collection ID are returned
    by `filter_prompts_by_collection`.
    """
    prompts = [
        create_prompt(collection_id='123'),
        create_prompt(collection_id='456'),
        create_prompt(collection_id='123')
    ]
    filtered_prompts = filter_prompts_by_collection(prompts, '123')
    assert len(filtered_prompts) == 2
    assert all(p.collection_id == '123' for p in filtered_prompts)

def test_search_prompts():
    """
    Test searching functionality of prompts based on query string.

    Ensures that prompts with the query string in their title or description
    are returned by `search_prompts`.
    """
    prompts = [
        create_prompt(title="Hello World", description="Example description"),
        create_prompt(title="Another Story", description="Another example")
    ]
    results = search_prompts(prompts, "hello")
    assert len(results) == 1
    assert results[0].title == "Hello World"

def test_search_prompts_empty_query():
    """
    Test searching functionality with an empty query string.

    Ensures that no prompts are returned when an empty query is provided.
    """
    prompts = [
        create_prompt(title="Hello World", description="Example description"),
        create_prompt(title="Another Story", description="Another example")
    ]
    results = search_prompts(prompts, "")
    assert len(results) == 0

def test_search_prompts_case_insensitivity():
    """
    Test searching functionality is case-insensitive.
    """
    prompts = [
        create_prompt(title="Hello World", description="Example description"),
        create_prompt(title="Another Story", description="Another example")
    ]
    results = search_prompts(prompts, "HELLO")
    assert len(results) == 1
    assert results[0].title == "Hello World"

def test_search_prompts_no_description():
    """
    Test searching functionality for prompts without a description.
    """
    prompts = [
        create_prompt(title="Alone", description=None),
        create_prompt(title="Silent", description=None)
    ]
    results = search_prompts(prompts, "alone")
    assert len(results) == 1
    assert results[0].title == "Alone"

def test_validate_prompt_content():
    """
    Test validation of prompt content.

    Confirms that `validate_prompt_content` rejects invalid content and
    accepts content meeting the criteria.
    """
    assert not validate_prompt_content("   ")
    assert not validate_prompt_content("short")
    assert validate_prompt_content("Valid prompt content")

def test_extract_variables():
    """
    Test extraction of template variables from content.

    Checks that `extract_variables` accurately extracts variable names
    enclosed in double curly braces from the content.
    """
    content = "Hello, {{name}}! Your account number is {{account_number}}."
    variables = extract_variables(content)
    assert variables == ["name", "account_number"]

def test_extract_variables_no_matches():
    """
    Test variable extraction when no matches present.

    Validates that the `extract_variables` function returns an empty list
    when there are no variables to extract in the content.
    """
    content = "Hello, world!"
    variables = extract_variables(content)
    assert variables == []

def test_extract_variables_edge_cases():
    """
    Test extraction of variables with edge cases in content.

    Ensures `extract_variables` handles consecutive and boundary variables
    correctly.
    """
    content = "{{start}} {{middle}} {{end}}"
    variables = extract_variables(content)
    assert variables == ["start", "middle", "end"]

