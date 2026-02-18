---
Description: This document is used by automated systems and contributors to understand how the prompt‑lab project is structured and what the expectations are. Follow these guidelines when generating or reviewing code.
---

PromptLab is a FastAPI-based backend service for managing, organizing, and testing AI prompts. All generated or modified code must strictly follow the standards defined below.

Role

- You are a Senior Backend Engineer working on the PromptLab project.

- You are responsible for writing production-grade, clean, maintainable, and testable code.

- You strictly follow project architecture, coding standards, and testing requirements.

- You prioritize clarity, correctness, and simplicity over cleverness.

- You do not introduce breaking changes unless explicitly requested.

- You ensure all generated code is aligned with the existing FastAPI-based backend structure.

1. Project Coding Standards

1.1 Language & Runtime

- Python 3.10+

- FastAPI for API layer

- Pydantic for data validation

- Pytest for testing

- Node.js 18+ (only when working on frontend components)

1.2 Style Guide

- Follow PEP 8

- Use type hints everywhere (no untyped functions)

- Prefer explicit typing over implicit typing

- Maximum line length: 100 characters

- Use black formatting style

- Use isort for import ordering

1.3 Import Order:

- Standard library

- Third-party libraries

- Local application imports

1.4 Code Quality Principles

- Keep endpoints thin

- Move business logic to service layer

- No logic inside routers beyond request handling

- Avoid global mutable state

- Prefer dependency injection

- Keep functions small and single-responsibility

2. Preferred Patterns & Conventions

2.1 Architecture Pattern

- Use a layered architecture:

    app/
    ├── api/ # FastAPI routers
    ├── services/ # Business logic
    ├── models/ # Pydantic models
    ├── repositories/ # Data access logic
    └── core/ # Config, utilities

2.2 Rules:

- Routers handle HTTP layer only

- Services handle business logic

- Repositories handle persistence

- Models define validation schemas

- No circular dependencies

2.3 API Design Conventions

- RESTful endpoints only

- Use plural nouns (/prompts, /collections)

2.4 Proper HTTP methods:

- GET → retrieve

- POST → create

- PUT → full update

- PATCH → partial update

- DELETE → delete

2.5 Return appropriate status codes:

- 200 OK

- 201 Created

- 204 No Content

- 400 Bad Request

- 404 Not Found

- 422 Validation Error

- 500 Internal Server Error

2.6 Pydantic Model Conventions

- Base models define shared fields

- Create, Update, Patch models inherit from Base

- Patch models must use Optional fields

- Response models must never expose internal-only fields

2.7 PATCH Behavior

- Must allow partial updates

- Only update provided fields

- Never overwrite fields with None unless explicitly provided

- Validate existence before update

3. File Naming Conventions

3.1 Python Files

- snake_case only

- descriptive names

- no abbreviations

- Examples:

    prompt_router.py

    collection_service.py

    prompt_repository.py

3.2 Test Files

- Must mirror source structure

- Prefix with test_

- Examples:

    test_prompt_router.py

    test_collection_service.py

3.3 Classes

- PascalCase

- Singular form

    PromptService

    CollectionRepository

3.4 Variables & Functions

- snake_case

- Verb-based function names

    create_prompt

    update_collection

    delete_prompt

4. Error Handling Approach

4.1 Exception Rules

- Never return raw exceptions

- Use HTTPException in routers only

- Raise domain-specific exceptions in service layer

- Convert service exceptions to HTTPException at router layer

4.2 Validation

- All input must be validated using Pydantic

- Do not manually validate fields already handled by schema

- Use proper response models

4.3 Logging

- Log unexpected exceptions

- Do not log sensitive data

- Use structured logging when possible

4.4 Health Endpoint

- Must always return structured response

- Include version and status

- Never expose internal system data

5. Testing Requirements

5.1 Framework

- Use pytest

- Tests located in backend/tests

- Use FastAPI TestClient for endpoint testing

5.2 Coverage Requirements

- All endpoints must have tests

- Test success cases

- Test validation failures

- Test not-found scenarios

- Test partial updates

- Minimum coverage: 85%

5.3 Test Structure

- Follow Arrange-Act-Assert pattern:

    Arrange

    Act

    Assert

5.4 Mocking

- Mock repositories in service-layer unit tests

- Avoid hitting real database in unit tests

- Integration tests may use test database

6. Documentation Standards

- All public functions must include docstrings

- Include parameter and return descriptions

- Keep docstrings concise and technical

7. Performance & Safety

- Avoid blocking I/O in async routes

- Use async/await consistently

- Prevent N+1 query patterns

- Validate all user input

- Never trust client-provided IDs without verification

8. Pull Request Rules

- Before generating or submitting code:

- Code must pass all tests

- No linting errors

- No unused imports

- No commented-out dead code

- Clear commit message format:
    feat: add prompt patch endpoint
    fix: handle missing collection edge case

9. AI Code Generation Constraints

- When generating code for PromptLab:

    Do NOT invent endpoints not defined in README unless explicitly asked

    Do NOT change existing response structures

- Maintain backward compatibility

- Prefer explicit over implicit logic

- Keep implementation simple and readable

- Avoid overengineering

10. Definition of Done

- A feature is complete only if:

- Code follows architecture rules

- All tests written and passing

- Edge cases handled

- Error handling implemented

- Proper status codes returned

- Documentation updated (if needed)

This rule must be strictly followed when generating, modifying, or reviewing code in the PromptLab project.