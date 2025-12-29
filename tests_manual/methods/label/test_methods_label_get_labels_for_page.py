# -*- coding: utf-8 -*-

from sanhe_confluence_sdk.methods.label.get_labels_for_page import (
    GetLabelsForPageRequest,
    GetLabelsForPageRequestPathParams,
    GetLabelsForPageRequestQueryParams,
)

from sanhe_confluence_sdk.tests import client, debug_prop, PAGE_ID


def test(
    mute,  # on separate line for easy comment in/out
):
    res = GetLabelsForPageRequest(
        path_params=GetLabelsForPageRequestPathParams(id=int(PAGE_ID)),
    ).sync(client)

    # --- GetLabelsForPageResponse level ---
    debug_prop(res.results)
    debug_prop(res.links)

    # --- GetLabelsForPageResponseLinks level ---
    debug_prop(res.links.next)
    debug_prop(res.links.base)

    # --- GetLabelsForPageResponseResult level (use first result if available) ---
    # Note: The page may have no labels, so check if results is not empty
    if res.results:
        result = res.results[0]
        debug_prop(result.id)
        debug_prop(result.name)
        debug_prop(result.prefix)


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.label.get_labels_for_page",
        preview=False,
    )
