# -*- coding: utf-8 -*-

from sanhe_confluence_sdk.methods.descendant.get_page_descendants import (
    GetPageDescendantsRequest,
    GetPageDescendantsRequestPathParams,
    GetPageDescendantsRequestQueryParams,
)
from sanhe_confluence_sdk.methods.space.get_space import (
    GetSpaceRequest,
    GetSpaceRequestPathParams,
)

from sanhe_confluence_sdk.tests import client, debug_prop, SPACE_ID


def test(
    mute,  # on separate line for easy comment in/out
):
    res = GetSpaceRequest(
        path_params=GetSpaceRequestPathParams(id=int(SPACE_ID)),
    ).sync(client)
    res = GetPageDescendantsRequest(
        path_params=GetPageDescendantsRequestPathParams(id=int(res.homepageId)),
        query_params=GetPageDescendantsRequestQueryParams(depth=5, limit=250),
    ).sync(client)

    # --- GetPageDescendantsResponse level ---
    debug_prop(res.results)
    debug_prop(res.links)

    # --- GetPageDescendantsResponseLinks level ---
    debug_prop(res.links.next)
    debug_prop(res.links.base)

    # --- GetPageDescendantsResponseResult level ---
    # Note: results may be empty if the page has no descendants
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
        "sanhe_confluence_sdk.methods.descendant.get_page_descendants",
        preview=False,
    )
