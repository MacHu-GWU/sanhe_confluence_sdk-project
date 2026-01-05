# -*- coding: utf-8 -*-

"""
Manual test for DeleteFolderRequest API method.

Note: This test deletes a real folder in Confluence, so it should be run
manually with extreme caution.

IMPORTANT: For POST/PATCH/DELETE/PUT (write) requests, ALL test code must be
commented out to prevent accidental damage to real Confluence data.
"""

from sanhe_confluence_sdk.methods.folder.delete_folder import (
    DeleteFolderRequest,
    DeleteFolderRequestPathParams,
)

from sanhe_confluence_sdk.tests import client, debug_prop


def test(
    mute,  # on separate line for easy comment in/out
):
    """
    Test DeleteFolderRequest API.

    IMPORTANT: This test is fully commented out because it deletes real data.
    To run the test:
    1. Create a test folder first (or use an existing disposable folder)
    2. Uncomment the test code below
    3. Run the test
    4. Re-comment the test code

    Note: DELETE requests return 204 No Content with no response body.
    The sync() method returns a DeleteFolderResponse object with empty _raw_data.
    """
    # --- Uncomment below to run actual test ---
    # folder_id = 123456789  # Replace with actual folder ID to delete
    #
    # res = DeleteFolderRequest(
    #     path_params=DeleteFolderRequestPathParams(id=folder_id),
    # ).sync(client)
    #
    # # Verify successful deletion
    # print(f"Response status code: {res.http_res.status_code}")
    # assert res.http_res.status_code == 204
    pass


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.folder.delete_folder",
        preview=False,
    )
