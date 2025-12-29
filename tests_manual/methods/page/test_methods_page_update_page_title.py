# -*- coding: utf-8 -*-

"""
Manual test for UpdatePageTitleRequest API method.

Note: This test updates a real page title in Confluence, so it should be run
manually with caution.

IMPORTANT: For POST/PATCH/DELETE/PUT (write) requests, ALL test code must be
commented out to prevent accidental damage to real Confluence data.
"""

from sanhe_confluence_sdk.methods.page.update_page_title import (
    UpdatePageTitleRequest,
    UpdatePageTitleRequestPathParams,
    UpdatePageTitleRequestBodyParams,
)

from sanhe_confluence_sdk.tests import client, debug_prop


def test(
    mute,  # on separate line for easy comment in/out
):
    """
    Test UpdatePageTitleRequest API.

    IMPORTANT: This test is fully commented out because it modifies real data.
    To run the test:
    1. Find a test page ID using GetPagesRequest
    2. Uncomment the test code below
    3. Run the test
    4. Re-comment the test code
    """
    # --- Uncomment below to run actual test ---
    # page_id = 123456789  # Replace with actual page ID
    #
    # res = UpdatePageTitleRequest(
    #     path_params=UpdatePageTitleRequestPathParams(
    #         id=page_id,
    #     ),
    #     body_params=UpdatePageTitleRequestBodyParams(
    #         status="current",  # or "draft"
    #         title="Updated Page Title",
    #     ),
    # ).sync(client)
    #
    # # --- UpdatePageTitleResponse level ---
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
    # # --- UpdatePageTitleResponseVersion level ---
    # debug_prop(res.version.createdAt)
    # debug_prop(res.version.message)
    # debug_prop(res.version.number)
    # debug_prop(res.version.minorEdit)
    # debug_prop(res.version.authorId)
    #
    # # --- UpdatePageTitleResponseBody level ---
    # debug_prop(res.body.storage)
    # debug_prop(res.body.atlas_doc_format)
    # debug_prop(res.body.view)
    #
    # # --- UpdatePageTitleResponseBodyStorage level ---
    # # debug_prop(res.body.storage.representation)  # body may be NA
    # # debug_prop(res.body.storage.value)  # body may be NA
    #
    # # --- UpdatePageTitleResponseBodyAtlasDocFormat level ---
    # # debug_prop(res.body.atlas_doc_format.representation)  # may be NA
    # # debug_prop(res.body.atlas_doc_format.value)  # may be NA
    #
    # # --- UpdatePageTitleResponseBodyView level ---
    # # debug_prop(res.body.view.representation)  # may be NA
    # # debug_prop(res.body.view.value)  # may be NA
    #
    # # --- UpdatePageTitleResponseLinks level ---
    # debug_prop(res.links.webui)
    # debug_prop(res.links.editui)
    # debug_prop(res.links.tinyui)
    pass


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.page.update_page_title",
        preview=False,
    )
