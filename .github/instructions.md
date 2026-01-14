## Code Assistant Instructions

### Architecture and Design

**Domain-Driven Design (DDD)**

* Organize code following DDD principles: clearly separate Domain, Application, Infrastructure, and Presentation layers.
* Identify and model aggregates, entities, and value objects within the domain.
* Keep business logic isolated in the domain layer, independent of frameworks and implementation details.

**Dependency Injection**

* Always use dependency injection to manage dependencies between components.
* Leverage FastAPI’s native DI system (`Depends`) for route handlers and services.
* Create interfaces/protocols for key dependencies (repositories, external services) to facilitate testing and maintenance.
* Avoid direct instantiations of concrete classes within other classes.

### Strong Typing

**Mandatory Type Hints**

* **Every** function, method, and variable must have explicit type hints.
* Always specify the return type of functions, including `-> None` where applicable.
* Never use `Any` unless absolutely necessary — document the reason when it’s unavoidable.
* Prefer specific types over generic types (e.g., `list[str]` instead of `list`).

**Advanced Type Hints**

* Use `typing.Protocol` to define structural interfaces.
* Utilize `TypeVar`, `Generic` for type-safe generic code.
* Use `Literal`, `Union`, `Optional` to precisely express possible types.
* Implement `TypedDict` for dictionaries with a known structure.
* Use `NewType` to create semantic type aliases (e.g., `UserId = NewType('UserId', int)`).

**Runtime Validation**

* Combine Pydantic models with type hints for runtime validation.
* Use `from __future__ import annotations` for forward references.
* Configure mypy in strict mode and ensure it passes without errors.
* Consider using `@overload` for functions with multiple signatures.

**Good Typing Examples**

```python
from typing import Protocol, TypeVar, Generic
from collections.abc import Sequence

class Repository(Protocol[T]):
    async def get(self, id: int) -> T | None: ...
    async def save(self, entity: T) -> T: ...

async def process_items(
    items: Sequence[Item],
    processor: Callable[[Item], Awaitable[Result]]
) -> list[Result]:
    ...
```

### Testing

**Test Structure**

* Write tests using test tables (parametrize) to cover multiple scenarios with DRY code.
* Explicitly cover non-optimal paths: edge cases, invalid values, network errors, timeouts, exceptions.
* Test both happy path and unhappy path for each feature.
* Type test cases as well: fixtures, parameters, and assertions should have type hints.

**Test Execution**

* Configure tests for parallel execution when possible (pytest-xdist).
* Before considering any modification complete, run `make test` and ensure all tests pass 100%.
* Tests must be fast, isolated, and deterministic.

### Quality Assurance

**Linting and Formatting**

* Always run `make lint` at the end of modifications.
* **ABSOLUTE RULE**: NEVER use `# type: ignore`, `# noqa`, `# pylint: disable` or similar suppression directives.
* Every warning or error from the linter must be fixed at the root, not hidden.
* If an error seems unsolvable, reconsider the architecture or logic rather than ignoring it.

**Type Checking**
* Include type checking in the `make lint` process or as a separate command.

**Mandatory Make Commands**
All of the following commands must complete without errors before considering the work finished:

* `make test` - all tests must pass.
* `make lint` - no linting/formatting/type checking errors.

**A task is NOT complete until all of these commands pass successfully.**

### Language

**English Only**

* All code, documentation, README files, inline comments, tests, commit messages, PR descriptions, and other repository-visible text must be written in English.
* Write code identifiers and comments clearly in English to ensure global team readability and consistent code reviews.
* If a translation or localized text is required for end-user content, include both English and the localized version in the appropriate resource files, and document the choice in the README.

### FastAPI Best Practices

**Endpoints**

* Use Pydantic models for request/response validation with complete type hints.
* Clearly define HTTP status codes for each scenario.
* Document endpoints with docstrings and examples in Pydantic models.
* Explicitly type injected dependencies with `Annotated[Type, Depends(...)]`.

**Async/Await**

* Prefer async handlers when interacting with I/O (database, external APIs).
* Use async-native libraries where possible (httpx, asyncpg, motor).
* Correctly type coroutines with `Awaitable`, `Coroutine`, or `async def`.

**Error Handling**

* Create custom exception handlers for domain-specific errors with type hints.
* Return structured (Pydantic models) and informative responses in case of error.
* Do not expose stack traces or implementation details in production.