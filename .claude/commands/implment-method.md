---
description: Implement a new Confluence API method from official documentation URL
argument-hint: <API_DOC_URL> <OPTIONAL_REQUIREMENTS>
---

Implement the Confluence API method described at: $ARGUMENTS

## Prerequisites

First, read the architecture guide to understand the codebase patterns:

- @docs/source/02-Maintainer-Guide/index.rst

## Reference Examples

Use these files as implementation templates (organized by common patterns):

| Pattern | Source Code | Test Code |
|---------|-------------|-----------|
| **GET list** (query_params only) | @sanhe_confluence_sdk/methods/space/get_spaces.py | @tests_manual/methods/space/test_methods_space_get_spaces.py |
| **GET by ID** (path_params + query_params) | @sanhe_confluence_sdk/methods/space/get_space.py | @tests_manual/methods/space/test_methods_space_get_space.py |
| **POST create** (body_params, optional query_params) | @sanhe_confluence_sdk/methods/page/create_page.py | @tests_manual/methods/page/test_methods_page_create_page.py |
| **PUT update** (path_params + body_params) | @sanhe_confluence_sdk/methods/page/update_page.py | @tests_manual/methods/page/test_methods_page_update_page.py |
| **DELETE** (path_params + query_params) | @sanhe_confluence_sdk/methods/page/delete_page.py | @tests_manual/methods/page/test_methods_page_delete_page.py |

**Shared Classes:**

- Links class for pagination: @sanhe_confluence_sdk/methods/common/links.py

## Implementation Steps

1. **Fetch API Documentation**
   - Read the official documentation at the given URL
   - Extract: HTTP method, endpoint path, path parameters, query parameters, request body schema, and response schema

2. **Reference OpenAPI Spec (Optional)**
   - Check `https://dac-static.atlassian.com/cloud/confluence/openapi-v2.v3.json` for additional schema details
   - Note: The spec may have errors - use official docs as the source of truth

3. **Create Module File**
   - Determine the API group (e.g., `space`, `page`, `content`)
   - Create: `sanhe_confluence_sdk/methods/{group}/{method_name}.py`
   - Follow snake_case naming for the filename

4. **Implement Parameter Classes**

   Define separate classes for each parameter type using `api_field()`:

   - `api_field(OPT)` - optional field, API key same as Python attr
   - `api_field(OPT, "apiKeyName")` - optional field with different API key (camelCase, kebab-case)
   - `api_field(REQ)` - required field
   - `api_field(REQ, "apiKeyName")` - required field with different API key

   ```python
   # Path parameters (for endpoints like /pages/{id})
   @dataclasses.dataclass(frozen=True)
   class {MethodName}RequestPathParams(PathParams):
       id: int = api_field(REQ)

   # Query parameters
   @dataclasses.dataclass(frozen=True)
   class {MethodName}RequestQueryParams(QueryParams):
       status: str = api_field(OPT)
       body_format: str = api_field(OPT, "body-format")  # kebab-case

   # Body parameters (for POST/PUT/PATCH)
   @dataclasses.dataclass(frozen=True)
   class {MethodName}RequestBodyParams(BodyParams):
       space_id: str = api_field(REQ, "spaceId")  # camelCase
       title: str = api_field(OPT)
       # Nested objects use dict type, NOT nested dataclasses
       body: T.Dict[str, T.Any] = api_field(OPT)
   ```

5. **Implement Request Class**

   Compose parameter classes - NO need to implement `_params` or `_body` (inherited from BaseRequest):

   ```python
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
       body_params: {MethodName}RequestBodyParams = dataclasses.field(
           default_factory={MethodName}RequestBodyParams
       )

       @property
       def _path(self) -> str:
           return f"/endpoint/{self.path_params.id}"

       def sync(self, client: Confluence) -> "{MethodName}Response":
           return self._sync_get({MethodName}Response, client)  # or _sync_post, _sync_put, _sync_delete
   ```

   - Add docstring with **only** the official docs URL (no parameter descriptions needed)
   - Only include parameter classes that are needed (e.g., GET list may only need `query_params`)

6. **Implement Response Classes**
   - Define nested classes from **deepest to shallowest** (bottom-up order)
   - Use long CamelCase names reflecting JSON path (e.g., `GetSpacesResponseResultDescription`)
   - Use `@cached_property` for all properties
   - Use `_get()` for primitive fields, `_new()` for objects, `_new_many()` for arrays
   - Use "happy path" type hints (no Optional, no NA in return types)
   - **For paginated list endpoints**: Import shared `Links` class from `..common.links` for top-level `_links`
   - **For DELETE requests**: Create an empty Response class (DELETE returns 204 No Content with empty `_raw_data`)

7. **Create Test File**
   - Create: `tests_manual/methods/{group}/test_methods_{group}_{method_name}.py`
   - Test all properties are accessible using `debug_prop()`
   - Comment out nested properties if parent object is `None` with a note
   - **CRITICAL: For POST/PATCH/PUT/DELETE requests, ALL test code must be commented out** to prevent damage to real Confluence data
   - **Mute fixture format**: Place `mute` on its own line with trailing comma for easy comment in/out:
     ```python
     def test(
         mute,  # on separate line for easy comment in/out
     ):
     ```

8. **Run and Verify**
   - For GET requests: Execute the test to ensure all accessible properties work
   - For POST/PATCH/PUT/DELETE: Only verify imports work (test code is commented out)
   - Check coverage report for any missed properties

## For Type Hints

- API keyword arguments / nested objects in request body: use `T.Dict[str, T.Any]`
- List of objects: use `list[{ItemType}]`

## Optional Requirements

$ARGUMENTS
