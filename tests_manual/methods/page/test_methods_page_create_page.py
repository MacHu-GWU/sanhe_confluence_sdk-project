# -*- coding: utf-8 -*-

"""
Manual test for CreatePageRequest API method.

Note: This test creates a real page in Confluence, so it should be run
manually and the page should be deleted afterwards.

IMPORTANT: For POST/PATCH/DELETE (write) requests, ALL test code must be
commented out to prevent accidental damage to real Confluence data.
"""

from sanhe_confluence_sdk.methods.page.create_page import CreatePageRequest

from sanhe_confluence_sdk.tests import client, debug_prop


def test(
    mute,  # on separate line for easy comment in/out
):
    """
    Test CreatePageRequest API.

    IMPORTANT: This test is fully commented out because it creates real data.
    To run the test:
    1. Uncomment the test code below
    2. Run the test
    3. Delete the created page manually after testing
    4. Re-comment the test code
    """
    # --- Uncomment below to run actual test ---
    # import uuid
    # unique_suffix = uuid.uuid4().hex[:8]
    #
    # # You need to provide a valid space_id from your Confluence instance
    # space_id = "YOUR_SPACE_ID"
    #
    # res = CreatePageRequest(
    #     space_id=space_id,
    #     status="current",
    #     title=f"Test Page {unique_suffix}",
    #     body={
    #         "representation": "storage",
    #         "value": "<p>Test page created by sanhe_confluence_sdk</p>",
    #     },
    # ).sync(client)
    #
    # # --- CreatePageResponse level ---
    # debug_prop(res.id)
    # debug_prop(res.status)
    # debug_prop(res.title)
    # debug_prop(res.spaceId)
    # debug_prop(res.parentId)
    # debug_prop(res.parentType)
    # debug_prop(res.position)
    # debug_prop(res.authorId)
    # debug_prop(res.ownerId)
    # debug_prop(res.lastOwnerId)
    # debug_prop(res.subtype)
    # debug_prop(res.createdAt)
    # debug_prop(res.version)
    # debug_prop(res.body)
    # debug_prop(res.links)
    #
    # # --- CreatePageResponseVersion level ---
    # debug_prop(res.version.createdAt)
    # debug_prop(res.version.message)
    # debug_prop(res.version.number)
    # debug_prop(res.version.minorEdit)
    # debug_prop(res.version.authorId)
    #
    # # --- CreatePageResponseBody level ---
    # # debug_prop(res.body.storage)  # body may be None
    # # debug_prop(res.body.atlas_doc_format)  # body may be None
    # # debug_prop(res.body.view)  # body may be None
    #
    # # --- CreatePageResponseBodyStorage level ---
    # # debug_prop(res.body.storage.representation)  # body may be None
    # # debug_prop(res.body.storage.value)  # body may be None
    #
    # # --- CreatePageResponseBodyAtlasDocFormat level ---
    # # debug_prop(res.body.atlas_doc_format.representation)  # body may be None
    # # debug_prop(res.body.atlas_doc_format.value)  # body may be None
    #
    # # --- CreatePageResponseBodyView level ---
    # # debug_prop(res.body.view.representation)  # body may be None
    # # debug_prop(res.body.view.value)  # body may be None
    #
    # # --- CreatePageResponseLinks level ---
    # debug_prop(res.links.webui)
    # debug_prop(res.links.editui)
    # debug_prop(res.links.tinyui)
    #
    # print(f"\nCreated page with id: {res.id}")
    # print(f"Remember to delete the page after testing!")
    pass


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.page.create_page",
        preview=False,
    )
