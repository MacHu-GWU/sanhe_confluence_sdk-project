# -*- coding: utf-8 -*-

"""
Manual test for DeletePageRequest API method.

Note: This test deletes a real page in Confluence, so it should be run
manually with extreme caution.

IMPORTANT: For POST/PATCH/DELETE/PUT (write) requests, ALL test code must be
commented out to prevent accidental damage to real Confluence data.
"""

from sanhe_confluence_sdk.methods.page.delete_page import (
    DeletePageRequest,
    DeletePageRequestPathParams,
    DeletePageRequestQueryParams,
)

from sanhe_confluence_sdk.tests import client, debug_prop


def test(
    mute,  # on separate line for easy comment in/out
):
    """
    Test DeletePageRequest API.

    IMPORTANT: This test is fully commented out because it deletes real data.
    To run the test:
    1. Create a test page first (or use an existing disposable page)
    2. Uncomment the test code below
    3. Run the test
    4. Re-comment the test code

    Note: DELETE requests return 204 No Content with no response body.
    The sync() method returns the httpx.Response object directly.
    """
    # --- Uncomment below to run actual test ---
    # page_id = 123456789  # Replace with actual page ID to delete
    #
    # # Basic delete (moves page to trash)
    # res = DeletePageRequest(
    #     path_params=DeletePageRequestPathParams(id=page_id),
    # ).sync(client)
    #
    # # Verify successful deletion
    # print(f"Response status code: {res.status_code}")
    # assert res.status_code == 204
    #
    # --- Alternative: Delete a draft page ---
    # res = DeletePageRequest(
    #     path_params=DeletePageRequestPathParams(id=page_id),
    #     query_params=DeletePageRequestQueryParams(draft=True),
    # ).sync(client)

    # --- Alternative: Permanently delete (purge) a trashed page ---
    # res = DeletePageRequest(
    #     path_params=DeletePageRequestPathParams(id=page_id),
    #     query_params=DeletePageRequestQueryParams(purge=True),
    # ).sync(client)
    pass


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.page.delete_page",
        preview=False,
    )
