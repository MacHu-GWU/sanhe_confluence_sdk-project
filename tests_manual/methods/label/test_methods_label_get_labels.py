# -*- coding: utf-8 -*-

from sanhe_confluence_sdk.methods.label.get_labels import (
    GetLabelsRequest,
    GetLabelsRequestQueryParams,
)

from sanhe_confluence_sdk.tests import client, debug_prop


def test(
    mute,  # on separate line for easy comment in/out
):
    res = GetLabelsRequest().sync(client)

    # --- GetLabelsResponse level ---
    debug_prop(res.results)
    debug_prop(res.links)

    # --- GetLabelsResponseLinks level ---
    debug_prop(res.links.next)
    debug_prop(res.links.base)

    # --- GetLabelsResponseResult level (use first result if exists) ---
    if res.results:
        result = res.results[0]
        debug_prop(result.id)
        debug_prop(result.name)
        debug_prop(result.prefix)


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.label.get_labels",
        preview=False,
    )
