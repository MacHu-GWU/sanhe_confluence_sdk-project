# -*- coding: utf-8 -*-

from sanhe_confluence_sdk.methods.page.get_pages_in_space import (
    GetPagesInSpaceRequest,
    GetPagesInSpaceRequestPathParams,
    GetPagesInSpaceRequestQueryParams,
)

from sanhe_confluence_sdk.tests import client, debug_prop, SPACE_ID


def test(
    mute,
):
    res = GetPagesInSpaceRequest(
        path_params=GetPagesInSpaceRequestPathParams(id=int(SPACE_ID)),
    ).sync(client)

    # --- GetPagesInSpaceResponse level ---
    debug_prop(res.results)
    debug_prop(res.links)

    # --- Links level ---
    debug_prop(res.links.next)
    debug_prop(res.links.base)

    # --- GetPagesInSpaceResponseResult level (use first result) ---
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

    # --- GetPagesInSpaceResponseResultVersion level ---
    debug_prop(result.version.createdAt)
    debug_prop(result.version.message)
    debug_prop(result.version.number)
    debug_prop(result.version.minorEdit)
    debug_prop(result.version.authorId)

    # --- GetPagesInSpaceResponseResultBody level ---
    # debug_prop(result.body.storage)  # body may be NA without body-format param
    # debug_prop(result.body.atlas_doc_format)  # body may be NA without body-format param

    # --- GetPagesInSpaceResponseResultBodyStorage level ---
    # debug_prop(result.body.storage.representation)  # body may be NA
    # debug_prop(result.body.storage.value)  # body may be NA

    # --- GetPagesInSpaceResponseResultBodyAtlasDocFormat level ---
    # debug_prop(result.body.atlas_doc_format.representation)  # body may be NA
    # debug_prop(result.body.atlas_doc_format.value)  # body may be NA

    # --- GetPagesInSpaceResponseResultLinks level ---
    debug_prop(result.links.webui)
    debug_prop(result.links.editui)
    debug_prop(result.links.tinyui)


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.page.get_pages_in_space",
        preview=False,
    )
