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
This module defines the foundation::

    api_field(default, wire_name=None)

A factory function that simplifies defining request parameters with automatic key conversion:

- ``default``: Use ``REQ`` for required fields, ``OPT`` for optional fields
- ``wire_name``: The API key name if different from Python attribute name (e.g., ``"spaceId"`` for ``space_id``)

.. code-block:: python

    # API key same as Python attr: "status" -> "status"
    status: str = api_field(OPT)

    # API key is camelCase: "space_id" -> "spaceId"
    space_id: str = api_field(REQ, "spaceId")

    # API key uses hyphen: "root_level" -> "root-level"
    root_level: bool = api_field(OPT, "root-level")

**PathParams, QueryParams, BodyParams**

Base classes for organizing request parameters by type:

- ``PathParams``: Parameters embedded in the URL path (e.g., ``/pages/{id}``)
- ``QueryParams``: URL query parameters (e.g., ``?limit=10&status=current``)
- ``BodyParams``: JSON request body fields (for POST/PUT/PATCH)

Each has a ``to_api_kwargs()`` method that automatically:

1. Removes optional (``OPT``) sentinel values
2. Converts Python attribute names to API key names using ``wire_name``

**BaseRequest**

- Composes three parameter objects: ``path_params``, ``query_params``, ``body_params``
- ``_path`` property returns the API endpoint path (e.g., ``/spaces/{id}``)
- ``_params`` property calls ``query_params.to_api_kwargs()`` to get processed query parameters
- ``_body`` property calls ``body_params.to_api_kwargs()`` to get processed request body
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
Each method module (e.g., ``page/create_page.py``) follows this structure:

**1. Parameter Classes (QueryParams, BodyParams, PathParams)**

Define separate classes for each parameter type. Use ``api_field()`` to define fields:

- ``api_field(OPT)`` - optional field, API key same as Python attr
- ``api_field(OPT, "apiKeyName")`` - optional field with different API key
- ``api_field(REQ, "apiKeyName")`` - required field with different API key

.. code-block:: python

    from ..model import api_field, BaseRequest, QueryParams, BodyParams, PathParams, BaseResponse

    # --- Query Parameters ---
    @dataclasses.dataclass(frozen=True)
    class CreatePageRequestQueryParams(QueryParams):
        embedded: bool = api_field(OPT)
        private: bool = api_field(OPT)
        root_level: bool = api_field(OPT, "root-level")


    # --- Body Parameters ---
    @dataclasses.dataclass(frozen=True)
    class CreatePageRequestBodyParams(BodyParams):
        space_id: str = api_field(REQ, "spaceId")
        status: str = api_field(OPT)
        title: str = api_field(OPT)
        parent_id: str = api_field(OPT, "parentId")
        # Nested objects use dict type, NOT nested dataclasses
        body: T.Dict[str, T.Any] = api_field(OPT)

**2. Request Class**

The docstring should contain **only** the official documentation URL. Compose the parameter classes:

.. code-block:: python

    @dataclasses.dataclass(frozen=True)
    class CreatePageRequest(BaseRequest):
        """
        See: https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/#api-pages-post
        """

        query_params: CreatePageRequestQueryParams = dataclasses.field(
            default_factory=CreatePageRequestQueryParams
        )
        body_params: CreatePageRequestBodyParams = dataclasses.field(
            default_factory=CreatePageRequestBodyParams
        )

        @property
        def _path(self) -> str:
            return "/pages"

        def sync(self, client: Confluence) -> "CreatePageResponse":
            return self._sync_post(CreatePageResponse, client)

**2b. Request with Path Parameters**

For endpoints with path parameters (e.g., ``/pages/{id}``), define a ``PathParams`` class and use it in ``_path``:

.. code-block:: python

    @dataclasses.dataclass(frozen=True)
    class GetPageRequestPathParams(PathParams):
        id: int = api_field(REQ)


    @dataclasses.dataclass(frozen=True)
    class GetPageRequestQueryParams(QueryParams):
        body_format: str = api_field(OPT, "body-format")
        version: int = api_field(OPT)


    @dataclasses.dataclass(frozen=True)
    class GetPageRequest(BaseRequest):
        """
        See: https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/#api-pages-id-get
        """

        path_params: GetPageRequestPathParams = dataclasses.field(
            default_factory=GetPageRequestPathParams
        )
        query_params: GetPageRequestQueryParams = dataclasses.field(
            default_factory=GetPageRequestQueryParams
        )

        @property
        def _path(self) -> str:
            return f"/pages/{self.path_params.id}"

        def sync(self, client: Confluence) -> "GetPageResponse":
            return self._sync_get(GetPageResponse, client)

**2c. DELETE Request**

DELETE requests typically return ``204 No Content`` with no response body. The ``_sync`` method handles this automatically:

.. code-block:: python

    @dataclasses.dataclass(frozen=True)
    class DeletePageRequestPathParams(PathParams):
        id: int = api_field(REQ)


    @dataclasses.dataclass(frozen=True)
    class DeletePageRequestQueryParams(QueryParams):
        purge: bool = api_field(OPT)
        draft: bool = api_field(OPT)


    @dataclasses.dataclass(frozen=True)
    class DeletePageRequest(BaseRequest):
        """
        See: https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/#api-pages-id-delete
        """

        path_params: DeletePageRequestPathParams = dataclasses.field(
            default_factory=DeletePageRequestPathParams
        )
        query_params: DeletePageRequestQueryParams = dataclasses.field(
            default_factory=DeletePageRequestQueryParams
        )

        @property
        def _path(self) -> str:
            return f"/pages/{self.path_params.id}"

        def sync(self, client: Confluence) -> "DeletePageResponse":
            return self._sync_delete(DeletePageResponse, client)


    # DELETE returns 204 No Content, so response class is empty
    @dataclasses.dataclass(frozen=True)
    class DeletePageResponse(BaseResponse):
        """Response for deleting a page."""
        pass

**Usage Examples:**

.. code-block:: python

    # POST request with body
    res = CreatePageRequest(
        body_params=CreatePageRequestBodyParams(
            space_id="12345",
            title="My Page",
            body={
                "representation": "storage",
                "value": "<p>Hello World</p>",
            },
        ),
    ).sync(client)

    # GET request with path and query params
    res = GetPageRequest(
        path_params=GetPageRequestPathParams(id=123456789),
        query_params=GetPageRequestQueryParams(body_format="storage"),
    ).sync(client)

    # DELETE request
    res = DeletePageRequest(
        path_params=DeletePageRequestPathParams(id=123456789),
        query_params=DeletePageRequestQueryParams(purge=True),
    ).sync(client)
    assert res.http_res.status_code == 204

**3. Response Classes (deepest nested first)**

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
**Parameter Class Names**

- ``{MethodName}RequestPathParams`` - path parameters
- ``{MethodName}RequestQueryParams`` - query parameters
- ``{MethodName}RequestBodyParams`` - body parameters

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


Pagination Utility
------------------------------------------------------------------------------
The ``sanhe_confluence_sdk/pagi.py`` module provides a generic ``paginate()`` function for iterating through paginated list endpoints.

**How Confluence Pagination Works:**

- Response contains ``_links.next`` with relative URL for next page (if more data exists)
- Response contains ``_links.base`` with the base URL
- Items are in the ``results`` field
- Page size is controlled by ``limit`` query parameter

**The ``paginate()`` Function:**

.. code-block:: python

    from sanhe_confluence_sdk.pagi import paginate
    from sanhe_confluence_sdk.methods.space.get_spaces import (
        GetSpacesRequest,
        GetSpacesResponse,
    )

    # Iterate through all spaces, 10 per page, up to 100 items
    for response in paginate(
        client=client,
        request=GetSpacesRequest(),
        response_type=GetSpacesResponse,
        page_size=10,
        max_items=100,
    ):
        for space in response.results:
            print(space.name)

**Parameters:**

- ``client``: Confluence client instance
- ``request``: Initial request object (must have ``query_params``)
- ``response_type``: Response class for deserialization
- ``page_size``: Number of items per page (sets the ``limit`` query parameter)
- ``max_items``: Stop fetching when total items >= this value
- ``max_pages``: Maximum pages to fetch (default 100, safeguard against infinite loops)
- ``limit_field``: Name of limit parameter (default ``"limit"``)
- ``results_field``: Name of results field in response (default ``"results"``)

**Parameter Validation:**

- ``page_size`` must be >= 1
- ``max_pages`` must be >= 1
- If ``max_items < page_size``, it's automatically adjusted to ``page_size`` (you always get at least one full page)

**Exceptions:**

- ``PaginationError``: Base exception for pagination errors
- ``MissingLinksError``: Raised when response doesn't have expected ``links`` attribute

**Implementation Details:**

The function uses ``dataclasses.replace()`` to immutably modify the request's ``query_params`` with the desired ``page_size``. It yields response objects (not individual items), allowing the caller to access both the items and response metadata.

.. code-block:: python

    # The paginator modifies query_params immutably
    request = dataclasses.replace(
        request,
        query_params=dataclasses.replace(
            request.query_params,
            limit=page_size,  # or custom limit_field
        ),
    )

**Loop Structure:**

.. code-block:: python

    # First request
    response = request.sync(client)
    yield response

    # Subsequent requests (at most max_pages - 1)
    for _ in range(max_pages - 1):
        # Check stop conditions
        if n_fetched_items >= max_items:
            break
        if not isinstance(response.links.next, str):
            break  # No more pages

        # Fetch next page using links.next URL
        url = client.url + response.links.next
        http_res = client.sync_client.get(url=url)
        response = response_type.from_success_http_response(http_res)
        yield response


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

**Example for POST/PATCH/DELETE Request** (``tests_manual/methods/page/test_methods_page_create_page.py``):

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
        3. Delete the created page manually after testing
        4. Re-comment the test code
        """
        # --- Uncomment below to run actual test ---
        # res = CreatePageRequest(
        #     body_params=CreatePageRequestBodyParams(
        #         space_id="12345",
        #         title="Test Page",
        #         body={
        #             "representation": "storage",
        #             "value": "<p>Test content</p>",
        #         },
        #     ),
        # ).sync(client)
        #
        # # --- CreatePageResponse level ---
        # debug_prop(res.id)
        # debug_prop(res.title)
        # debug_prop(res.spaceId)
        pass  # Keep only pass statement


Code Generation
------------------------------------------------------------------------------
The ``sanhe_confluence_sdk/methods/m.py`` module provides lazy-loading access to all Request/Response classes. This module is **auto-generated** and should not be edited manually.

**Regenerating m.py**

After adding or modifying API methods, run the code generator to update ``m.py``::

    make gen-m

Or directly::

    .venv/bin/python scripts/gen_m.py

**What the generator does:**

1. Scans ``sanhe_confluence_sdk/methods/`` subdirectories (``label/``, ``page/``, ``space/``, etc.)
2. Discovers all ``*Request`` and ``*Response`` classes
3. Validates that the classes exist and are importable
4. Generates ``m.py`` with lazy-loading properties for each class

**Files involved:**

- ``scripts/gen_m.py`` - The generator script
- ``scripts/m.py.jinja2`` - Jinja2 template for code generation
- ``sanhe_confluence_sdk/methods/m.py`` - Generated output (DO NOT EDIT)

**When to regenerate:**

- After creating a new API method module
- After renaming or deleting an existing method
- After modifying the ``m.py.jinja2`` template


Development Workflow
------------------------------------------------------------------------------
When implementing a new API method:

**1. Gather Information**

- Official docs URL (e.g., ``https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-space/#api-spaces-get``)
- OpenAPI spec JSON (reference only, may have errors): ``https://dac-static.atlassian.com/cloud/confluence/openapi-v2.v3.json``

**2. Reference Examples**

- GET request pattern: ``sanhe_confluence_sdk/methods/page/get_page.py``
- POST request pattern: ``sanhe_confluence_sdk/methods/page/create_page.py``
- PUT request pattern: ``sanhe_confluence_sdk/methods/page/update_page.py``
- DELETE request pattern: ``sanhe_confluence_sdk/methods/page/delete_page.py``
- GET test pattern: ``tests_manual/methods/space/test_methods_space_get_spaces.py``
- POST test pattern: ``tests_manual/methods/page/test_methods_page_create_page.py``
- DELETE test pattern: ``tests_manual/methods/page/test_methods_page_delete_page.py``

**3. Implementation Steps**

1. Create module file: ``methods/{group}/{method_name}.py``
2. Define ``PathParams`` class if endpoint has path parameters (use ``api_field(REQ)`` for required path params)
3. Define ``QueryParams`` class for query parameters (use ``api_field(OPT)`` or ``api_field(OPT, "wire-name")``)
4. Define ``BodyParams`` class for POST/PUT/PATCH body (use ``api_field(REQ, "wireName")`` for required, ``api_field(OPT)`` for optional)
5. Define ``Request`` class:
   - Add docstring with **only** the official docs URL
   - Compose parameter classes with ``dataclasses.field(default_factory=...)``
   - Implement ``_path`` property (use ``self.path_params.id`` etc. for path parameters)
   - Implement ``sync()`` method using ``_sync_get``, ``_sync_post``, ``_sync_put``, or ``_sync_delete``
6. Add Response classes (deepest nested first)
7. Use ``_get`` for primitives, ``_new`` for objects, ``_new_many`` for arrays
8. For paginated list endpoints, import ``Links`` from ``..common.links`` for top-level ``_links``
9. Create test file: ``tests_manual/methods/{group}/test_methods_{group}_{method_name}.py``
10. For GET requests: run test, comment out properties where parent is ``None``
11. For POST/PATCH/DELETE: comment out ALL test code, keep only ``pass``
12. Run ``make gen-m`` to regenerate ``m.py`` with the new Request/Response classes

**4. Key Patterns to Remember**

- All dataclasses use ``frozen=True`` for immutability
- Use ``api_field(REQ, "wireName")`` for required fields, ``api_field(OPT)`` for optional
- Use ``wire_name`` parameter when API key differs from Python attr (camelCase, kebab-case, etc.)
- All response properties use ``@cached_property`` for lazy loading
- In request body, use ``dict`` type for nested objects (not nested dataclasses)
- Define response nested classes before parent classes (bottom-up)
- For paginated endpoints, use shared ``Links`` class (import from ``..common.links``)
- DELETE requests return a Response object with empty ``_raw_data`` (204 No Content)
- Comment out ALL test code for POST/PATCH/DELETE requests


Quick Reference
------------------------------------------------------------------------------
**GET Request Template:**

.. code-block:: python

    @dataclasses.dataclass(frozen=True)
    class {MethodName}RequestPathParams(PathParams):
        id: int = api_field(REQ)


    @dataclasses.dataclass(frozen=True)
    class {MethodName}RequestQueryParams(QueryParams):
        param1: str = api_field(OPT)
        param_two: int = api_field(OPT, "param-two")  # kebab-case in API


    @dataclasses.dataclass(frozen=True)
    class {MethodName}Request(BaseRequest):
        """
        See: {official_docs_url}
        """

        path_params: {MethodName}RequestPathParams = dataclasses.field(
            default_factory={MethodName}RequestPathParams
        )
        query_params: {MethodName}RequestQueryParams = dataclasses.field(
            default_factory={MethodName}RequestQueryParams
        )

        @property
        def _path(self) -> str:
            return f"/endpoint/{self.path_params.id}"

        def sync(self, client: Confluence) -> "{MethodName}Response":
            return self._sync_get({MethodName}Response, client)

**POST/PUT/PATCH Request Template:**

.. code-block:: python

    @dataclasses.dataclass(frozen=True)
    class {MethodName}RequestQueryParams(QueryParams):
        serialize_ids: bool = api_field(OPT, "serialize-ids-as-strings")


    @dataclasses.dataclass(frozen=True)
    class {MethodName}RequestBodyParams(BodyParams):
        name: str = api_field(REQ)
        space_id: str = api_field(REQ, "spaceId")
        # Nested objects use dict, NOT nested dataclasses
        description: T.Dict[str, str] = api_field(OPT)
        items: T.List[T.Dict[str, T.Any]] = api_field(OPT)


    @dataclasses.dataclass(frozen=True)
    class {MethodName}Request(BaseRequest):
        """
        See: {official_docs_url}
        """

        query_params: {MethodName}RequestQueryParams = dataclasses.field(
            default_factory={MethodName}RequestQueryParams
        )
        body_params: {MethodName}RequestBodyParams = dataclasses.field(
            default_factory={MethodName}RequestBodyParams
        )

        @property
        def _path(self) -> str:
            return "/endpoint"

        def sync(self, client: Confluence) -> "{MethodName}Response":
            return self._sync_post({MethodName}Response, client)

**DELETE Request Template:**

.. code-block:: python

    @dataclasses.dataclass(frozen=True)
    class {MethodName}RequestPathParams(PathParams):
        id: int = api_field(REQ)


    @dataclasses.dataclass(frozen=True)
    class {MethodName}RequestQueryParams(QueryParams):
        purge: bool = api_field(OPT)


    @dataclasses.dataclass(frozen=True)
    class {MethodName}Request(BaseRequest):
        """
        See: {official_docs_url}
        """

        path_params: {MethodName}RequestPathParams = dataclasses.field(
            default_factory={MethodName}RequestPathParams
        )
        query_params: {MethodName}RequestQueryParams = dataclasses.field(
            default_factory={MethodName}RequestQueryParams
        )

        @property
        def _path(self) -> str:
            return f"/endpoint/{self.path_params.id}"

        def sync(self, client: Confluence) -> "{MethodName}Response":
            return self._sync_delete({MethodName}Response, client)


    # DELETE returns 204 No Content, so response class is empty
    @dataclasses.dataclass(frozen=True)
    class {MethodName}Response(BaseResponse):
        """Response for {method_name}."""
        pass

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
        res = {MethodName}Request(
            path_params={MethodName}RequestPathParams(id=123),
        ).sync(client)

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
        #     body_params={MethodName}RequestBodyParams(
        #         name="Test",
        #         description={"value": "desc", "representation": "plain"},
        #     ),
        # ).sync(client)
        #
        # debug_prop(res.field1)
        # debug_prop(res.nested)
        pass
