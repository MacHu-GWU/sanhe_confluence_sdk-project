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

- All request parameters are dataclass attributes with ``default=OPT`` (optional)
- ``_path`` property returns the API endpoint path (e.g., ``/spaces``)
- ``_params`` property maps Python attributes to API parameter names (handles ``snake_case`` → ``kebab-case`` conversion)
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

.. code-block:: python

    @dataclasses.dataclass(frozen=True)
    class GetSpacesRequest(BaseRequest):
        """
        See: https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-space/#api-spaces-get
        """

        # All parameters default to OPT (optional)
        ids: list[int] = dataclasses.field(default=OPT)
        keys: list[str] = dataclasses.field(default=OPT)
        limit: int = dataclasses.field(default=OPT)

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
Tests live in ``tests_manual/`` and use real Confluence data:

**Test Style:**

- Only test that properties are **accessible** without exceptions
- Don't assert on **values** - they change and we can't control them
- If parent object is ``None``, comment out child property tests with a note

**Example** (``tests_manual/test_methods_space_get_spaces.py``):

.. code-block:: python

    def test(mute):  # mute fixture silences debug_prop output
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

- Use ``mute`` in test signature to silence ``debug_prop`` output during CI
- Remove ``mute`` when debugging to see all property values


Development Workflow
------------------------------------------------------------------------------
When implementing a new API method:

**1. Gather Information**

- Official docs URL (e.g., ``https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-space/#api-spaces-get``)
- OpenAPI spec JSON (reference only, may have errors): ``https://dac-static.atlassian.com/cloud/confluence/openapi-v2.v3.json``

**2. Reference Examples**

- Request pattern: ``sanhe_confluence_sdk/methods/space/get_spaces.py``
- Test pattern: ``tests_manual/test_methods_space_get_spaces.py``

**3. Implementation Steps**

1. Create module file: ``methods/{group}/{method_name}.py``
2. Add Request class with all query/path parameters (all ``default=OPT``)
3. Add docstring with official docs URL
4. Implement ``_path``, ``_params``, and ``sync()`` method
5. Add Response classes (deepest nested first)
6. Use ``_get`` for primitives, ``_new`` for objects, ``_new_many`` for arrays
7. Create test file: ``tests_manual/test_methods_{group}_{method_name}.py``
8. Run test, comment out any properties where parent is ``None``

**4. Key Patterns to Remember**

- All dataclasses use ``frozen=True`` for immutability
- All request attributes use ``dataclasses.field(default=OPT)``
- All response properties use ``@cached_property`` for lazy loading
- Map kebab-case API params to snake_case Python attrs in ``_params``
- Define nested classes before parent classes (bottom-up)


Quick Reference
------------------------------------------------------------------------------
**Request Class Template:**

.. code-block:: python

    @dataclasses.dataclass(frozen=True)
    class {MethodName}Request(BaseRequest):
        """
        See: {official_docs_url}
        """

        param1: str = dataclasses.field(default=OPT)
        param2: int = dataclasses.field(default=OPT)

        @property
        def _path(self) -> str:
            return "/endpoint"

        @property
        def _params(self):
            return {
                "param1": self.param1,
                "param-2": self.param2,  # kebab-case in API
            }

        def sync(self, client: Confluence) -> "{MethodName}Response":
            return self._sync_get({MethodName}Response, client)

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

**Test Template:**

.. code-block:: python

    def test(mute):
        res = {MethodName}Request().sync(client)

        debug_prop(res.field1)
        debug_prop(res.nested)
        debug_prop(res.items)

        # debug_prop(res.nested.child)  # nested is None
