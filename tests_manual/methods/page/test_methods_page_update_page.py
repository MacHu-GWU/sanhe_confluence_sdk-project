# -*- coding: utf-8 -*-

"""
Manual test for UpdatePageRequest API method.

Note: This test updates a real page in Confluence, so it should be run
manually with caution.

IMPORTANT: For POST/PATCH/DELETE/PUT (write) requests, ALL test code must be
commented out to prevent accidental damage to real Confluence data.
"""

from sanhe_confluence_sdk.methods.page.update_page import UpdatePageRequest

from sanhe_confluence_sdk.tests import client, debug_prop


def test(
    mute,  # on separate line for easy comment in/out
):
    """
    Test UpdatePageRequest API.

    IMPORTANT: This test is fully commented out because it modifies real data.
    To run the test:
    1. Find a test page ID using GetPagesRequest
    2. Uncomment the test code below
    3. Run the test
    4. Re-comment the test code
    """
    # --- Uncomment below to run actual test ---
    # # First, you need to get an existing page to know its current version
    # # Use GetPagesRequest or GetPageByIdRequest to get the page first
    #
    # page_id = 123456789  # Replace with actual page ID
    # current_version = 1  # Replace with actual current version number
    #
    # res = UpdatePageRequest(
    #     id=page_id,
    #     status="current",
    #     title="Updated Page Title",
    #     body={
    #         "representation": "storage",
    #         "value": "<p>Updated content</p>",
    #     },
    #     version={
    #         "number": current_version + 1,
    #         "message": "Updated via sanhe_confluence_sdk",
    #     },
    # ).sync(client)
    #
    # # --- UpdatePageResponse level ---
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
    # # --- UpdatePageResponseVersion level ---
    # debug_prop(res.version.createdAt)
    # debug_prop(res.version.message)
    # debug_prop(res.version.number)
    # debug_prop(res.version.minorEdit)
    # debug_prop(res.version.authorId)
    #
    # # --- UpdatePageResponseBody level ---
    # debug_prop(res.body.storage)
    # debug_prop(res.body.atlas_doc_format)
    # debug_prop(res.body.view)
    #
    # # --- UpdatePageResponseBodyStorage level ---
    # debug_prop(res.body.storage.representation)
    # debug_prop(res.body.storage.value)
    #
    # # --- UpdatePageResponseBodyAtlasDocFormat level ---
    # # debug_prop(res.body.atlas_doc_format.representation)  # may be None
    # # debug_prop(res.body.atlas_doc_format.value)  # may be None
    #
    # # --- UpdatePageResponseBodyView level ---
    # # debug_prop(res.body.view.representation)  # may be None
    # # debug_prop(res.body.view.value)  # may be None
    #
    # # --- UpdatePageResponseLinks level ---
    # debug_prop(res.links.webui)
    # debug_prop(res.links.editui)
    # debug_prop(res.links.tinyui)
    pass


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.page.update_page",
        preview=False,
    )
