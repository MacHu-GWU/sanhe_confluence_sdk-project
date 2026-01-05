# -*- coding: utf-8 -*-

from sanhe_confluence_sdk.methods.children.get_folder_direct_children import (
    GetFolderDirectChildrenRequest,
    GetFolderDirectChildrenRequestPathParams,
    GetFolderDirectChildrenRequestQueryParams,
)

from sanhe_confluence_sdk.tests import client, debug_prop, FOLDER_ID


def test(
    mute,  # on separate line for easy comment in/out
):
    res = GetFolderDirectChildrenRequest(
        path_params=GetFolderDirectChildrenRequestPathParams(id=int(FOLDER_ID)),
    ).sync(client)

    # --- GetFolderDirectChildrenResponse level ---
    debug_prop(res.results)
    debug_prop(res.links)

    # --- GetFolderDirectChildrenResponseLinks level ---
    debug_prop(res.links.next)
    debug_prop(res.links.base)

    # --- GetFolderDirectChildrenResponseResult level (use first result if available) ---
    if res.results:
        result = res.results[0]
        debug_prop(result.id)
        debug_prop(result.status)
        debug_prop(result.title)
        debug_prop(result.type)
        debug_prop(result.spaceId)
        debug_prop(result.childPosition)


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.children.get_folder_direct_children",
        preview=False,
    )
