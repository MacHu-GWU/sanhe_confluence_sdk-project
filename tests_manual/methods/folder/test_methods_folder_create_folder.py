# -*- coding: utf-8 -*-

"""
Manual test for CreateFolderRequest API method.

Note: This test creates a real folder in Confluence, so it should be run
manually and the folder should be deleted afterwards.

IMPORTANT: For POST/PATCH/DELETE (write) requests, ALL test code must be
commented out to prevent accidental damage to real Confluence data.
"""

from sanhe_confluence_sdk.methods.folder.create_folder import (
    CreateFolderRequest,
    CreateFolderRequestBodyParams,
)

from sanhe_confluence_sdk.tests import client, debug_prop, SPACE_ID


def test(
    mute,  # on separate line for easy comment in/out
):
    """
    Test CreateFolderRequest API.

    IMPORTANT: This test is fully commented out because it creates real data.
    To run the test:
    1. Uncomment the test code below
    2. Run the test
    3. Delete the created folder manually after testing
    4. Re-comment the test code
    """
    # --- Uncomment below to run actual test ---
    # import uuid
    # unique_suffix = uuid.uuid4().hex[:8]
    # res = CreateFolderRequest(
    #     body_params=CreateFolderRequestBodyParams(
    #         space_id=SPACE_ID,
    #         title=f"Test Folder - {unique_suffix}",
    #     ),
    # ).sync(client)

    # --- CreateFolderResponse level ---
    # debug_prop(res)
    # debug_prop(res.id)
    # debug_prop(res.type)
    # debug_prop(res.status)
    # debug_prop(res.title)
    # debug_prop(res.parentId)
    # debug_prop(res.parentType)
    # debug_prop(res.position)
    # debug_prop(res.authorId)
    # debug_prop(res.ownerId)
    # debug_prop(res.createdAt)
    # debug_prop(res.spaceId)
    # debug_prop(res.version)
    # debug_prop(res.links)

    # --- CreateFolderResponseVersion level ---
    # debug_prop(res.version.createdAt)
    # debug_prop(res.version.message)
    # debug_prop(res.version.number)
    # debug_prop(res.version.minorEdit)
    # debug_prop(res.version.authorId)

    # --- CreateFolderResponseLinks level ---
    # debug_prop(res.links.webui)
    #
    # print(f"\nCreated folder with id: {res.id}")
    # print(f"Remember to delete the folder after testing!")
    pass


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.folder.create_folder",
        preview=False,
    )
