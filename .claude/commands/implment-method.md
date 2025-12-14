---
description: Implement a new Confluence API method from official documentation URL
argument-hint: <API_DOC_URL>
---

Implement the Confluence API method described at: $ARGUMENTS

## Prerequisites

First, read the architecture guide to understand the codebase patterns:

- @docs/source/02-Maintainer-Guide/index.rst

## Reference Examples

Use these files as implementation templates:

- Request/Response pattern: @sanhe_confluence_sdk/methods/space/get_spaces.py
- Test pattern: @tests_manual/test_methods_space_get_spaces.py

## Implementation Steps

1. **Fetch API Documentation**
   - Read the official documentation in the given URL
   - Extract: HTTP method, endpoint path, path parameters, query parameters, request body schema, and response schema

2. **Reference OpenAPI Spec (Optional)**
   - Check `https://dac-static.atlassian.com/cloud/confluence/openapi-v2.v3.json` for additional schema details
   - Note: The spec may have errors - use official docs as the source of truth

3. **Create Module File**
   - Determine the API group (e.g., `space`, `page`, `content`)
   - Create: `sanhe_confluence_sdk/methods/{group}/{method_name}.py`
   - Follow snake_case naming for the filename

4. **Implement Request Class**
   - Add all path parameters, query parameters, and request body fields as dataclass attributes
   - All attributes should use `dataclasses.field(default=OPT)`
   - Implement `_path` property (include path parameters)
   - Implement `_params` property (map snake_case attrs to API parameter names)
   - Implement `_body` property if request has body (for POST/PATCH/PUT)
   - Implement `sync()` method using appropriate `_sync_get`, `_sync_post`, etc.
   - Add docstring with the official docs URL

5. **Implement Response Classes**
   - Define nested classes from **deepest to shallowest** (bottom-up order)
   - Use long CamelCase names reflecting JSON path (e.g., `GetSpacesResponseResultDescription`)
   - Use `@cached_property` for all properties
   - Use `_get()` for primitive fields, `_new()` for objects, `_new_many()` for arrays
   - Use "happy path" type hints (no Optional, no NA in return types)

6. **Create Test File**
   - Create: `tests_manual/test_methods_{group}_{method_name}.py`
   - Test all properties are accessible using `debug_prop()`
   - Comment out nested properties if parent object is `None` with a note

7. **Run and Verify**
   - Execute the test to ensure all accessible properties work
   - Check coverage report for any missed properties
