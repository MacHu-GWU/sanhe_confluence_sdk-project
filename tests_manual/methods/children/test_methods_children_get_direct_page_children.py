# -*- coding: utf-8 -*-

from sanhe_confluence_sdk.methods.children.get_direct_page_children import (
    GetDirectPageChildrenRequest,
    GetDirectPageChildrenRequestPathParams,
    GetDirectPageChildrenRequestQueryParams,
)

from sanhe_confluence_sdk.tests import client, debug_prop, PAGE_ID


def test(
    mute,  # on separate line for easy comment in/out
):
    res = GetDirectPageChildrenRequest(
        path_params=GetDirectPageChildrenRequestPathParams(id=int(PAGE_ID)),
    ).sync(client)

    # --- GetDirectPageChildrenResponse level ---
    debug_prop(res.results)
    debug_prop(res.links)

    # --- GetDirectPageChildrenResponseLinks level ---
    debug_prop(res.links.next)
    debug_prop(res.links.base)

    # --- GetDirectPageChildrenResponseResult level (use first result if available) ---
    # Note: results may be empty if the page has no direct children
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
        "sanhe_confluence_sdk.methods.children.get_direct_page_children",
        preview=False,
    )