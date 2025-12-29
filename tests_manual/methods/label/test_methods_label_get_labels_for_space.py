# -*- coding: utf-8 -*-

from sanhe_confluence_sdk.methods.label.get_labels_for_space import (
    GetLabelsForSpaceRequest,
    GetLabelsForSpaceRequestPathParams,
    GetLabelsForSpaceRequestQueryParams,
)

from sanhe_confluence_sdk.tests import client, debug_prop, SPACE_ID


def test(
    mute,  # on separate line for easy comment in/out
):
    res = GetLabelsForSpaceRequest(
        path_params=GetLabelsForSpaceRequestPathParams(id=int(SPACE_ID)),
    ).sync(client)

    # --- GetLabelsForSpaceResponse level ---
    debug_prop(res.results)
    debug_prop(res.links)

    # --- GetLabelsForSpaceResponseLinks level ---
    debug_prop(res.links.next)
    debug_prop(res.links.base)

    # --- GetLabelsForSpaceResponseResult level ---
    # Note: results may be empty if space has no labels
    if res.results:
        result = res.results[0]
        debug_prop(result.id)
        debug_prop(result.name)
        debug_prop(result.prefix)


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.label.get_labels_for_space",
        preview=False,
    )
