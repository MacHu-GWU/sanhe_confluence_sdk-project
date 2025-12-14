# -*- coding: utf-8 -*-

from sanhe_confluence_sdk.methods.page.get_pages import GetPagesRequest

from sanhe_confluence_sdk.tests import client, debug_prop


def test(mute):
    res = GetPagesRequest().sync(client)

    # --- GetPagesResponse level ---
    debug_prop(res.results)
    debug_prop(res.links)

    # --- GetPagesResponseLinks level ---
    debug_prop(res.links.next)
    debug_prop(res.links.base)

    # --- GetPagesResponseResult level (use first result) ---
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

    # --- GetPagesResponseResultVersion level ---
    debug_prop(result.version.createdAt)
    debug_prop(result.version.message)
    debug_prop(result.version.number)
    debug_prop(result.version.minorEdit)
    debug_prop(result.version.authorId)

    # --- GetPagesResponseResultBody level ---
    # debug_prop(result.body.storage)  # body may be None without body-format param
    # debug_prop(result.body.atlas_doc_format)  # body may be None without body-format param

    # --- GetPagesResponseResultBodyStorage level ---
    # debug_prop(result.body.storage.representation)  # body may be None
    # debug_prop(result.body.storage.value)  # body may be None

    # --- GetPagesResponseResultBodyAtlasDocFormat level ---
    # debug_prop(result.body.atlas_doc_format.representation)  # body may be None
    # debug_prop(result.body.atlas_doc_format.value)  # body may be None

    # --- GetPagesResponseResultLinks level ---
    debug_prop(result.links.webui)
    debug_prop(result.links.editui)
    debug_prop(result.links.tinyui)


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.page.get_pages",
        preview=False,
    )
