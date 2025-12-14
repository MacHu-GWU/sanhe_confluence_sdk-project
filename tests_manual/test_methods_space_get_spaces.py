# -*- coding: utf-8 -*-

from sanhe_confluence_sdk.methods.space.get_spaces import GetSpacesRequest

from sanhe_confluence_sdk.tests import client, debug_prop


def test(
    mute
):
    res = GetSpacesRequest().sync(client)

    # --- GetSpacesResponse level ---
    debug_prop(res.results)
    debug_prop(res.links)

    # --- GetSpacesResponseLinks level ---
    debug_prop(res.links.next)
    debug_prop(res.links.base)

    # --- GetSpacesResponseResult level (use first result) ---
    result = res.results[0]
    debug_prop(result.id)
    debug_prop(result.key)
    debug_prop(result.name)
    debug_prop(result.type)
    debug_prop(result.status)
    debug_prop(result.authorId)
    debug_prop(result.currentActiveAlias)
    debug_prop(result.createdAt)
    debug_prop(result.homepageId)
    debug_prop(result.description)
    debug_prop(result.icon)
    debug_prop(result.links)

    # --- GetSpacesResponseResultDescription level ---
    # debug_prop(result.description.plain)  # description is None
    # debug_prop(result.description.view)  # description is None

    # --- GetSpacesResponseResultDescriptionPlain level ---
    # debug_prop(result.description.plain.representation)  # description is None
    # debug_prop(result.description.plain.value)  # description is None

    # --- GetSpacesResponseResultDescriptionView level ---
    # debug_prop(result.description.view.representation)  # description is None
    # debug_prop(result.description.view.value)  # description is None

    # --- GetSpacesResponseResultIcon level ---
    # debug_prop(result.icon.path)  # icon is None
    # debug_prop(result.icon.apiDownloadLink)  # icon is None

    # --- GetSpacesResponseResultLinks level ---
    debug_prop(result.links.webui)


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.space.get_spaces",
        preview=False,
    )
