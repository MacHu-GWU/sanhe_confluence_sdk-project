Quick Start
==============================================================================


What is sanhe_confluence_sdk?
------------------------------------------------------------------------------

``sanhe_confluence_sdk`` is a Pythonic SDK for the Confluence REST API v2. It is designed with the following principles:

- **Everything is a Class**: All requests and responses are represented as Python dataclasses with full type hints.
- **IDE Friendly**: With complete type annotations, you get autocomplete and inline documentation in your IDE.
- **Access Raw Data**: Every response object has a ``.raw_data`` attribute that gives you the original JSON dictionary if needed.
- **Consistent Pattern**: All API calls follow the same pattern - create a Request, call ``.sync(client)``, get a Response.


Installation
------------------------------------------------------------------------------

.. code-block:: bash

    pip install sanhe-confluence-sdk


Create a Client
------------------------------------------------------------------------------

To interact with the Confluence API, you first need to create a ``Confluence`` client. Currently, the SDK supports authentication via API Token (Basic Auth).

.. code-block:: python

    from sanhe_confluence_sdk.api import Confluence

    # Create a client with your Confluence credentials
    # - url: Your Atlassian site URL (e.g., https://your-domain.atlassian.net)
    # - username: Your email address
    # - password: Your API token (create one at https://id.atlassian.com/manage-profile/security/api-tokens)
    client = Confluence(
        url="https://your-domain.atlassian.net",
        username="your-email@example.com",
        password="your-api-token",
    )


Basic Usage
------------------------------------------------------------------------------

All API methods follow the same pattern:

1. Import the ``m`` module which provides lazy-loading access to all Request/Response classes
2. Create a Request object with the desired parameters
3. Call ``request.sync(client)`` to execute the request
4. Get a typed Response object back

Example - Get All Spaces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from sanhe_confluence_sdk.api import Confluence, m

    # Create client
    client = Confluence(
        url="https://your-domain.atlassian.net",
        username="your-email@example.com",
        password="your-api-token",
    )

    # Create a request to get spaces
    request = m.GetSpacesRequest()

    # Execute the request
    response = request.sync(client)

    # Access the results - fully typed!
    for space in response.results:
        print(f"Space: {space.name} (key={space.key})")

    # Need the raw JSON? Use .raw_data
    print(response.raw_data)

Example - Get a Specific Page
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For requests that require path parameters, import the PathParams class from the specific module:

.. code-block:: python

    from sanhe_confluence_sdk.api import Confluence
    from sanhe_confluence_sdk.methods.page.get_page import (
        GetPageRequest,
        GetPageRequestPathParams,
    )

    client = Confluence(...)

    # Create a request with path parameters
    request = GetPageRequest(
        path_params=GetPageRequestPathParams(id=123456789),
    )

    response = request.sync(client)
    print(f"Page title: {response.title}")
    print(f"Page status: {response.status}")

Example - Create a New Page
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For requests that require body parameters, import the BodyParams class:

.. code-block:: python

    from sanhe_confluence_sdk.api import Confluence
    from sanhe_confluence_sdk.methods.page.create_page import (
        CreatePageRequest,
        CreatePageRequestBodyParams,
    )

    client = Confluence(...)

    # Create a request with body parameters
    request = CreatePageRequest(
        body_params=CreatePageRequestBodyParams(
            space_id="123456",
            title="My New Page",
            body={
                "representation": "storage",
                "value": "<p>Hello, Confluence!</p>",
            },
        ),
    )

    response = request.sync(client)
    print(f"Created page: {response.id}")


Pagination
------------------------------------------------------------------------------

Many Confluence API endpoints return paginated results. The SDK provides a ``paginate()`` helper function to iterate through all pages of results.

.. code-block:: python

    from sanhe_confluence_sdk.api import Confluence, paginate
    from sanhe_confluence_sdk.methods.space.get_spaces import (
        GetSpacesRequest,
        GetSpacesResponse,
    )

    client = Confluence(...)

    # Create the initial request
    request = GetSpacesRequest()

    # Use paginate() to iterate through all pages
    for response in paginate(
        client=client,
        request=request,
        response_type=GetSpacesResponse,
        page_size=25,      # Number of items per page
        max_items=100,     # Stop after fetching this many items
    ):
        for space in response.results:
            print(f"Space: {space.name}")

The ``paginate()`` function parameters:

- ``client``: Your Confluence client instance
- ``request``: The initial request object
- ``response_type``: The Response class type (e.g., ``GetSpacesResponse``)
- ``page_size``: Number of items to fetch per page
- ``max_items``: Maximum total items to fetch (stops pagination when reached)
- ``max_pages``: Maximum number of pages to fetch (default: 100, safety limit)


What's Next?
------------------------------------------------------------------------------

- Check out the :ref:`API Reference <modindex>` for all available Request/Response classes
- Each Request class links to the official Atlassian API documentation in its docstring
