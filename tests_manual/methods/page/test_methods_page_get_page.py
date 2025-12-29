# -*- coding: utf-8 -*-

from sanhe_confluence_sdk.methods.page.get_page import (
    GetPageRequest,
    GetPageRequestPathParams,
    GetPageRequestQueryParams,
)

from sanhe_confluence_sdk.tests import client, debug_prop, PAGE_ID


def test(
    # mute,
):
    # Get the single page
    res = GetPageRequest(
        path_params=GetPageRequestPathParams(id=int(PAGE_ID)),
    ).sync(client)

    # --- GetPageResponse level ---
    debug_prop(res.id)
    debug_prop(res.status)
    debug_prop(res.title)
    debug_prop(res.spaceId)
    debug_prop(res.parentId)
    debug_prop(res.parentType)
    debug_prop(res.position)
    debug_prop(res.authorId)
    debug_prop(res.ownerId)
    debug_prop(res.lastOwnerId)
    debug_prop(res.subtype)
    debug_prop(res.createdAt)
    debug_prop(res.isFavoritedByCurrentUser)
    debug_prop(res.version)
    debug_prop(res.body)
    debug_prop(res.links)

    # --- GetPageResponseVersion level ---
    debug_prop(res.version.createdAt)
    debug_prop(res.version.message)
    debug_prop(res.version.number)
    debug_prop(res.version.minorEdit)
    debug_prop(res.version.authorId)

    # --- GetPageResponseBody level ---
    # debug_prop(res.body.storage)  # body may be None without body-format param
    # debug_prop(res.body.atlas_doc_format)  # body may be None without body-format param
    # debug_prop(res.body.view)  # body may be None without body-format param

    # --- GetPageResponseLinks level ---
    debug_prop(res.links.webui)
    debug_prop(res.links.editui)
    debug_prop(res.links.tinyui)

    # --- Optional include-* fields (not included by default) ---
    # debug_prop(res.labels)  # Only available when include-labels=true
    # debug_prop(res.properties)  # Only available when include-properties=true
    # debug_prop(res.operations)  # Only available when include-operations=true
    # debug_prop(res.likes)  # Only available when include-likes=true
    # debug_prop(res.versions)  # Only available when include-versions=true


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.page.get_page",
        preview=False,
    )
