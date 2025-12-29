# -*- coding: utf-8 -*-

"""
Manual test for GetPagesForLabelRequest API method.

Note: This test requires a valid label ID that has pages associated with it.
You may need to find a label ID first using the labels API.
"""

from sanhe_confluence_sdk.methods.page.get_pages_for_label import (
    GetPagesForLabelRequest,
    GetPagesForLabelRequestPathParams,
    GetPagesForLabelRequestQueryParams,
)

from sanhe_confluence_sdk.tests import client, debug_prop


# You'll need to find a valid label ID from your Confluence instance
# Labels can be found using the GET /pages/{id}/labels endpoint
LABEL_ID = 123456789  # Replace with actual label ID


def test(
    mute,
):
    res = GetPagesForLabelRequest(
        path_params=GetPagesForLabelRequestPathParams(id=LABEL_ID),
    ).sync(client)

    # --- GetPagesForLabelResponse level ---
    debug_prop(res.results)
    debug_prop(res.links)

    # --- GetPagesForLabelResponseLinks level ---
    debug_prop(res.links.next)
    debug_prop(res.links.base)

    # --- GetPagesForLabelResponseResult level (use first result) ---
    # Note: results may be empty if no pages have this label
    if res.results:
        result = res.results[0]
        debug_prop(result.id)
        debug_prop(result.status)
        debug_prop(result.title)
        debug_prop(result.spaceId)
        debug_prop(result.parentId)
        debug_prop(result.parentType)
        debug_prop(result.position)
        debug_prop(result.authorId)
        debug_prop(result.ownerId)
        debug_prop(result.lastOwnerId)
        debug_prop(result.subtype)
        debug_prop(result.createdAt)
        debug_prop(result.version)
        debug_prop(result.body)
        debug_prop(result.links)

        # --- GetPagesForLabelResponseResultVersion level ---
        debug_prop(result.version.createdAt)
        debug_prop(result.version.message)
        debug_prop(result.version.number)
        debug_prop(result.version.minorEdit)
        debug_prop(result.version.authorId)

        # --- GetPagesForLabelResponseResultBody level ---
        # debug_prop(result.body.storage)  # body may be NA without body-format param
        # debug_prop(result.body.atlas_doc_format)  # body may be NA without body-format param

        # --- GetPagesForLabelResponseResultBodyStorage level ---
        # debug_prop(result.body.storage.representation)  # body may be NA
        # debug_prop(result.body.storage.value)  # body may be NA

        # --- GetPagesForLabelResponseResultBodyAtlasDocFormat level ---
        # debug_prop(result.body.atlas_doc_format.representation)  # body may be NA
        # debug_prop(result.body.atlas_doc_format.value)  # body may be NA

        # --- GetPagesForLabelResponseResultLinks level ---
        debug_prop(result.links.webui)
        debug_prop(result.links.editui)
        debug_prop(result.links.tinyui)


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.page.get_pages_for_label",
        preview=False,
    )
