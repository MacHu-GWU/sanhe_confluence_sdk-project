Maintainer Guide
==============================================================================
This guide explains the architecture and design decisions of the ``sanhe_confluence_sdk`` library, helping maintainers understand the codebase and develop new API methods.


Why We Built This SDK
------------------------------------------------------------------------------
This library is a Python client for Confluence Cloud REST API v2. We chose to build it manually instead of using OpenAPI code generators because:

1. **Atlassian's OpenAPI spec has many errors** - The spec doesn't match actual API behavior
2. **Generated code produces too many bugs** - We tried code generators but the errors were overwhelming and impossible to fix systematically
3. **Documentation is unreliable** - Neither the OpenAPI spec nor the web documentation can be fully trusted

Given these constraints, we designed an architecture that:

- Uses **Command Pattern** for requests - all parameters as class attributes
- Uses **Lazy Load Pattern** for responses - ``cached_property`` for all fields so one broken field doesn't break others
- Provides **field-level autocomplete** as the primary goal - accuracy is a secondary concern since even Atlassian can't guarantee it


Core Architecture
------------------------------------------------------------------------------

Base Classes (``sanhe_confluence_sdk/methods/model.py``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module defines the foundation:

**BaseRequest**

- Request parameters are dataclass attributes with ``default=REQ`` (required) or ``default=OPT`` (optional)
- ``_path`` property returns the API endpoint path (e.g., ``/spaces``)
- ``_params`` property maps Python attributes to API query parameter names (handles ``snake_case`` → ``kebab-case`` conversion)
- ``_body`` property maps Python attributes to API request body fields (for POST/PUT/PATCH requests)
- ``_final_params`` property processes ``_params`` to remove optional/sentinel values before sending
- ``_final_body`` property processes ``_body`` to remove optional/sentinel values before sending
- ``sync()`` method wraps ``httpx`` GET/POST/PATCH/DELETE calls via ``_sync_get``, ``_sync_post``, etc.

**BaseResponse**

- ``_raw_data``: stores the raw JSON response dict
- ``_http_res``: stores the ``httpx.Response`` object for accessing HTTP metadata
- Users can always access underlying data even if a property is broken

Key methods for parsing JSON into typed properties:

- ``_get(field)``: returns primitive value, or ``NA`` sentinel if field absent
- ``_new(klass, field)``: creates single nested object from JSON object field
- ``_new_many(klass, field)``: creates list of nested objects from JSON array field

**NA Sentinel**

We use ``NA`` (Not Available) sentinel to distinguish three states:

1. Field exists with data → return the value/object
2. Field exists but is ``None`` → return ``None`` (explicit null in API)
3. Field is absent → return ``NA`` sentinel


Directory Structure
------------------------------------------------------------------------------
The ``sanhe_confluence_sdk/methods/`` directory mirrors the official API structure:

- Official docs: https://developer.atlassian.com/cloud/confluence/rest/v2/intro/#about
- Each **API group** (Space, Page, Content, etc.) → sub-package (``space/``, ``page/``, etc.)
- Each **API method** → module file (``get_spaces.py``, ``create_page.py``, etc.)

::

    sanhe_confluence_sdk/methods/
    ├── model.py              # Base classes
    ├── space/
    │   ├── __init__.py
    │   ├── get_spaces.py     # GET /spaces
    │   └── get_space.py      # GET /spaces/{id}
    ├── page/
    │   ├── __init__.py
    │   ├── get_pages.py      # GET /pages
    │   └── create_page.py    # POST /pages
    └── ...


Per-Method Module Structure
------------------------------------------------------------------------------
Each method module (e.g., ``space/get_spaces.py``) follows this structure:

**1. Request Class (first)**

The docstring should contain **only** the official documentation URL - no parameter descriptions are needed since users can refer to the official docs directly.

Use comments to separate different parameter types (path, query, body) and indicate whether they are required or optional. Use ``default=REQ`` for required parameters and ``default=OPT`` for optional parameters.

.. code-block:: python

    @dataclasses.dataclass(frozen=True)
    class GetSpacesRequest(BaseRequest):
        """
        See: https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-space/#api-spaces-get
        """

        # Query parameters (all optional for this endpoint)
        ids: list[int] = dataclasses.field(default=OPT)
        keys: list[str] = dataclasses.field(default=OPT)
        limit: int = dataclasses.field(default=OPT)
        description_format: str = dataclasses.field(default=OPT)

        @property
        def _path(self) -> str:
            return "/spaces"

        @property
        def _params(self):
            return {
                "ids": self.ids,
                "keys": self.keys,
                "limit": self.limit,
                # Note: API uses kebab-case, Python uses snake_case
                "description-format": self.description_format,
            }

        def sync(self, client: Confluence) -> "GetSpacesResponse":
            return self._sync_get(GetSpacesResponse, client)

**1b. Request Class with Body (POST/PUT/PATCH)**

For requests that send a body (POST, PUT, PATCH), add the ``_body`` property. Note that POST/PUT/PATCH requests may also have query parameters - always check the official docs and implement ``_params`` if needed.

Nested objects in the request body should be passed as **plain dicts**, not as nested dataclass instances. This keeps the API simple and avoids unnecessary complexity.

Use comments to clearly separate path parameters, query parameters, and body parameters:

.. code-block:: python

    @dataclasses.dataclass(frozen=True)
    class CreateSpaceRequest(BaseRequest):
        """
        See: https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-space/#api-spaces-post
        """

        # Query parameters (optional)
        serialize_ids_as_strings: bool = dataclasses.field(default=OPT)

        # Body parameters (required)
        name: str = dataclasses.field(default=REQ)
        key: str = dataclasses.field(default=REQ)

        # Body parameters (optional)
        create_private_space: bool = dataclasses.field(default=OPT)
        # Nested objects use dict type, NOT nested dataclasses
        description: T.Dict[str, str] = dataclasses.field(default=OPT)
        role_assignments: T.List[T.Dict[str, T.Any]] = dataclasses.field(default=OPT)

        @property
        def _path(self) -> str:
            return "/spaces"

        @property
        def _params(self):
            return {
                "serialize-ids-as-strings": self.serialize_ids_as_strings,
            }

        @property
        def _body(self):
            return {
                "name": self.name,
                "key": self.key,
                "description": self.description,  # dict passed through directly
                "roleAssignments": self.role_assignments,  # list of dicts
                "createPrivateSpace": self.create_private_space,
            }

        def sync(self, client: Confluence) -> "CreateSpaceResponse":
            return self._sync_post(CreateSpaceResponse, client)

**Usage example:**

.. code-block:: python

    # Nested objects are passed as plain dicts
    res = CreateSpaceRequest(
        name="My Space",
        key="MYSPACE",
        description={
            "value": "Space description",
            "representation": "plain",
        },
        role_assignments=[
            {
                "principal": {"principalType": "USER", "principalId": "abc123"},
                "roleId": "role-id",
            }
        ],
    ).sync(client)

**2. Response Classes (deepest nested first)**

Define nested classes from deepest to shallowest so type hints work without forward references:

.. code-block:: python

    # --- Deepest nested objects first ---
    @dataclasses.dataclass(frozen=True)
    class GetSpacesResponseResultDescriptionPlain(BaseResponse):
        @cached_property
        def representation(self) -> str:
            return self._get("representation")

        @cached_property
        def value(self) -> str:
            return self._get("value")


    @dataclasses.dataclass(frozen=True)
    class GetSpacesResponseResultDescription(BaseResponse):
        @cached_property
        def plain(self) -> GetSpacesResponseResultDescriptionPlain:
            return self._new(GetSpacesResponseResultDescriptionPlain, "plain")


    # --- Main result object ---
    @dataclasses.dataclass(frozen=True)
    class GetSpacesResponseResult(BaseResponse):
        @cached_property
        def id(self) -> str:
            return self._get("id")

        @cached_property
        def description(self) -> GetSpacesResponseResultDescription:
            return self._new(GetSpacesResponseResultDescription, "description")


    # --- Top level response ---
    @dataclasses.dataclass(frozen=True)
    class GetSpacesResponse(BaseResponse):
        @cached_property
        def results(self) -> list[GetSpacesResponseResult]:
            return self._new_many(GetSpacesResponseResult, "results")


Naming Conventions
------------------------------------------------------------------------------
**Response Class Names**

Use long names that reflect JSON path as CamelCase:

- ``results[]`` → ``GetSpacesResponseResult``
- ``results[].description`` → ``GetSpacesResponseResultDescription``
- ``results[].description.plain`` → ``GetSpacesResponseResultDescriptionPlain``
- ``_links`` → ``GetSpacesResponseLinks``

**Property Names**

- Simple fields: match JSON field name (``id``, ``key``, ``name``)
- Nested objects: use ``_new()`` with the nested class
- Arrays: use ``_new_many()`` with the element class
- JSON ``_links`` field → Python ``links`` property (remove underscore for cleaner API)


Common/Shared Classes
------------------------------------------------------------------------------
Some response classes are shared across multiple API methods and are defined in ``sanhe_confluence_sdk/methods/common/``:

**Links Class** (``sanhe_confluence_sdk/methods/common/links.py``)

For methods that return paginated results (e.g., ``GET /pages``, ``GET /spaces``), the top-level ``_links`` field uses a shared ``Links`` class:

.. code-block:: python

    from ..common.links import Links

    @dataclasses.dataclass(frozen=True)
    class GetPagesResponse(BaseResponse):
        @cached_property
        def results(self) -> list[GetPagesResponseResult]:
            return self._new_many(GetPagesResponseResult, "results")

        @cached_property
        def links(self) -> Links:
            return self._new(Links, "_links")

The ``Links`` class provides:

- ``next``: Relative URL for the next page of results (cursor pagination)
- ``base``: Base URL of the Confluence site

**When to use shared vs method-specific Links:**

- **Use shared ``Links``**: For top-level pagination links in list endpoints (``GET /pages``, ``GET /spaces``, etc.)
- **Use method-specific**: For nested ``_links`` objects within result items (e.g., ``GetPagesResponseResultLinks``)


Type Hints Philosophy
------------------------------------------------------------------------------
**Always use "happy path" types:**

- Don't use ``Optional[T]`` or ``T | None``
- Don't account for ``NA`` sentinel in return types
- The primary goal is **IDE autocomplete**, not runtime type accuracy

.. code-block:: python

    # Good - clean autocomplete
    @cached_property
    def id(self) -> str:
        return self._get("id")

    # Bad - pollutes autocomplete
    @cached_property
    def id(self) -> str | None | NA:
        return self._get("id")

**Why this works:**

- ``cached_property`` with ``_get``/``_new``/``_new_many`` provides defensive programming
- If a field is broken, only that property fails - not the entire response
- Users can always fall back to ``response.raw_data`` to access underlying JSON


Testing Strategy
------------------------------------------------------------------------------
Tests live in ``tests_manual/methods/{group}/`` and use real Confluence data:

**Test File Structure:**

::

    tests_manual/methods/
    ├── space/
    │   ├── all.py                                    # Run all tests in group
    │   ├── test_methods_space_get_spaces.py          # GET /spaces
    │   ├── test_methods_space_get_space.py           # GET /spaces/{id}
    │   └── test_methods_space_create_space.py        # POST /spaces
    ├── page/
    │   ├── all.py                                    # Run all tests in group
    │   └── test_methods_page_get_pages.py            # GET /pages
    └── ...

**Test Style:**

- Only test that properties are **accessible** without exceptions
- Don't assert on **values** - they change and we can't control them
- If parent object is ``None``, comment out child property tests with a note

**CRITICAL: Write Request Tests (POST/PATCH/DELETE)**

For any request that modifies data (POST, PATCH, PUT, DELETE), **ALL test code must be commented out** to prevent accidental damage to real Confluence data. This is irreversible!

- Write the test code as you would for a GET request
- Comment out ALL executable lines (keep only ``pass``)
- Add clear instructions for manual testing
- Never commit uncommitted test code for write operations

**Example for GET Request** (``tests_manual/methods/space/test_methods_space_get_spaces.py``):

.. code-block:: python

    def test(
        mute,  # mute fixture silences debug_prop output; on separate line for easy comment in/out
    ):
        res = GetSpacesRequest().sync(client)

        # --- GetSpacesResponse level ---
        debug_prop(res.results)
        debug_prop(res.links)

        # --- GetSpacesResponseResult level ---
        result = res.results[0]
        debug_prop(result.id)
        debug_prop(result.description)
        debug_prop(result.icon)

        # --- Nested levels ---
        # debug_prop(result.description.plain)  # description is None
        # debug_prop(result.icon.path)  # icon is None

**The ``mute`` fixture:**

- Place ``mute`` on its own line with a trailing comma (as shown above)
- This formatting allows easy comment in/out to toggle debug output
- Black formatter preserves this format (won't collapse to single line)
- Comment out ``mute,`` to see ``debug_prop`` output when debugging
- Keep ``mute,`` uncommented during CI/normal runs to silence output

**Example for POST/PATCH/DELETE Request** (``tests_manual/methods/space/test_methods_space_create_space.py``):

.. code-block:: python

    """
    IMPORTANT: For POST/PATCH/DELETE (write) requests, ALL test code must be
    commented out to prevent accidental damage to real Confluence data.
    """

    def test(
        mute,  # on separate line for easy comment in/out
    ):
        """
        IMPORTANT: This test is fully commented out because it creates real data.
        To run the test:
        1. Uncomment the test code below
        2. Run the test
        3. Delete the created space manually after testing
        4. Re-comment the test code
        """
        # --- Uncomment below to run actual test ---
        # res = CreateSpaceRequest(
        #     name="Test Space",
        #     key="TESTSPACE",
        #     description={
        #         "value": "Test description",
        #         "representation": "plain",
        #     },
        # ).sync(client)
        #
        # # --- CreateSpaceResponse level ---
        # debug_prop(res.id)
        # debug_prop(res.key)
        # debug_prop(res.name)
        pass  # Keep only pass statement


Development Workflow
------------------------------------------------------------------------------
When implementing a new API method:

**1. Gather Information**

- Official docs URL (e.g., ``https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-space/#api-spaces-get``)
- OpenAPI spec JSON (reference only, may have errors): ``https://dac-static.atlassian.com/cloud/confluence/openapi-v2.v3.json``

**2. Reference Examples**

- GET request pattern: ``sanhe_confluence_sdk/methods/space/get_spaces.py``
- POST request pattern: ``sanhe_confluence_sdk/methods/space/create_space.py``
- PUT request pattern (with path/query/body separation): ``sanhe_confluence_sdk/methods/page/update_page.py``
- GET test pattern: ``tests_manual/methods/space/test_methods_space_get_spaces.py``
- POST test pattern: ``tests_manual/methods/space/test_methods_space_create_space.py``

**3. Implementation Steps**

1. Create module file: ``methods/{group}/{method_name}.py``
2. Add Request class with path/query/body parameters, using ``default=REQ`` for required and ``default=OPT`` for optional
3. Use comments to separate path parameters, query parameters, and body parameters
4. Add docstring with **only** the official docs URL (no parameter descriptions)
5. Implement ``_path`` property
6. Implement ``_params`` property for query parameters (even for POST/PUT/PATCH if the API has them)
7. Implement ``_body`` property for request body (POST/PUT/PATCH only)
8. Implement ``sync()`` method using ``_sync_get``, ``_sync_post``, etc.
9. Add Response classes (deepest nested first)
10. Use ``_get`` for primitives, ``_new`` for objects, ``_new_many`` for arrays
11. For paginated list endpoints, import ``Links`` from ``..common.links`` for top-level ``_links``
12. Create test file: ``tests_manual/methods/{group}/test_methods_{group}_{method_name}.py``
13. For GET requests: run test, comment out properties where parent is ``None``
14. For POST/PATCH/DELETE: comment out ALL test code, keep only ``pass``

**4. Key Patterns to Remember**

- All dataclasses use ``frozen=True`` for immutability
- Required request attributes use ``dataclasses.field(default=REQ)``
- Optional request attributes use ``dataclasses.field(default=OPT)``
- Use comments to separate path parameters, query parameters, and body parameters in request classes
- POST/PUT/PATCH requests may have query parameters too - always implement ``_params`` if the API supports them
- All response properties use ``@cached_property`` for lazy loading
- Map kebab-case API params to snake_case Python attrs in ``_params`` and ``_body``
- In request body, use ``dict`` type for nested objects (not nested dataclasses)
- Define response nested classes before parent classes (bottom-up)
- For paginated endpoints, use shared ``Links`` class (import from ``..common.links``)
- Comment out ALL test code for POST/PATCH/DELETE requests


Quick Reference
------------------------------------------------------------------------------
**GET Request Template:**

.. code-block:: python

    @dataclasses.dataclass(frozen=True)
    class {MethodName}Request(BaseRequest):
        """
        See: {official_docs_url}
        """

        # Path parameters (required)
        id: int = dataclasses.field(default=REQ)

        # Query parameters (optional)
        param1: str = dataclasses.field(default=OPT)
        param2: int = dataclasses.field(default=OPT)

        @property
        def _path(self) -> str:
            return f"/endpoint/{self.id}"

        @property
        def _params(self):
            return {
                "param1": self.param1,
                "param-2": self.param2,  # kebab-case in API
            }

        def sync(self, client: Confluence) -> "{MethodName}Response":
            return self._sync_get({MethodName}Response, client)

**POST/PUT/PATCH Request Template:**

.. code-block:: python

    @dataclasses.dataclass(frozen=True)
    class {MethodName}Request(BaseRequest):
        """
        See: {official_docs_url}
        """

        # Path parameters (required)
        id: int = dataclasses.field(default=REQ)

        # Query parameters (optional)
        serialize_ids_as_strings: bool = dataclasses.field(default=OPT)

        # Body parameters (required)
        name: str = dataclasses.field(default=REQ)

        # Body parameters (optional)
        # Nested objects use dict, NOT nested dataclasses
        description: T.Dict[str, str] = dataclasses.field(default=OPT)
        items: T.List[T.Dict[str, T.Any]] = dataclasses.field(default=OPT)

        @property
        def _path(self) -> str:
            return f"/endpoint/{self.id}"

        @property
        def _params(self):
            return {
                "serialize-ids-as-strings": self.serialize_ids_as_strings,
            }

        @property
        def _body(self):
            return {
                "name": self.name,
                "description": self.description,
                "items": self.items,
            }

        def sync(self, client: Confluence) -> "{MethodName}Response":
            return self._sync_post({MethodName}Response, client)

**Response Class Template:**

.. code-block:: python

    @dataclasses.dataclass(frozen=True)
    class {MethodName}Response(BaseResponse):
        @cached_property
        def field1(self) -> str:
            return self._get("field1")

        @cached_property
        def nested(self) -> {MethodName}ResponseNested:
            return self._new({MethodName}ResponseNested, "nested")

        @cached_property
        def items(self) -> list[{MethodName}ResponseItem]:
            return self._new_many({MethodName}ResponseItem, "items")

**GET Test Template:**

.. code-block:: python

    def test(
        mute,  # on separate line for easy comment in/out
    ):
        res = {MethodName}Request().sync(client)

        debug_prop(res.field1)
        debug_prop(res.nested)
        debug_prop(res.items)

        # debug_prop(res.nested.child)  # nested is None

**POST/PATCH/DELETE Test Template (ALL code commented out):**

.. code-block:: python

    def test(
        mute,  # on separate line for easy comment in/out
    ):
        """
        IMPORTANT: This test is fully commented out because it modifies real data.
        To run the test:
        1. Uncomment the test code below
        2. Run the test
        3. Clean up any created data manually
        4. Re-comment the test code
        """
        # --- Uncomment below to run actual test ---
        # res = {MethodName}Request(
        #     name="Test",
        #     description={"value": "desc", "representation": "plain"},
        # ).sync(client)
        #
        # debug_prop(res.field1)
        # debug_prop(res.nested)
        pass
