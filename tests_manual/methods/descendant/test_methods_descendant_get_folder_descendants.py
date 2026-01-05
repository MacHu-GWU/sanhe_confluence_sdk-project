# -*- coding: utf-8 -*-

"""
Manual test for GetFolderDescendantsRequest API method.

Note: You need to have at least one folder in your Confluence space to run this test.
"""

from sanhe_confluence_sdk.methods.descendant.get_folder_descendants import (
    GetFolderDescendantsRequest,
    GetFolderDescendantsRequestPathParams,
    GetFolderDescendantsRequestQueryParams,
)

from sanhe_confluence_sdk.tests import client, debug_prop, FOLDER_ID


def test(
    # mute,  # on separate line for easy comment in/out
):
    res = GetFolderDescendantsRequest(
        path_params=GetFolderDescendantsRequestPathParams(id=int(FOLDER_ID)),
        query_params=GetFolderDescendantsRequestQueryParams(
            depth=2,
            limit=25,
        ),
    ).sync(client)

    # --- GetFolderDescendantsResponse level ---
    debug_prop(res.results)
    debug_prop(res.links)

    # --- GetFolderDescendantsResponseLinks level ---
    debug_prop(res.links.next)
    debug_prop(res.links.base)

    # --- GetFolderDescendantsResponseResult level ---
    # Note: results may be empty if the folder has no descendants
    if res.results:
        result = res.results[0]
        debug_prop(result.id)
        debug_prop(result.status)
        debug_prop(result.title)
        debug_prop(result.type)
        debug_prop(result.parentId)
        debug_prop(result.depth)
        debug_prop(result.childPosition)


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.descendant.get_folder_descendants",
        preview=False,
    )
