# -*- coding: utf-8 -*-

"""
Manual test for GetFolderRequest API method.

Note: You need to have at least one folder in your Confluence space to run this test.
Update the FOLDER_ID below with a valid folder ID from your Confluence instance.
"""

from sanhe_confluence_sdk.methods.folder.get_folder import (
    GetFolderRequest,
    GetFolderRequestPathParams,
    GetFolderRequestQueryParams,
)

from sanhe_confluence_sdk.tests import client, debug_prop, FOLDER_ID


def test(
    # mute,
):
    # Get the folder by ID with expanded fields
    res = GetFolderRequest(
        path_params=GetFolderRequestPathParams(id=int(FOLDER_ID)),
        query_params=GetFolderRequestQueryParams(
            include_operations=True,
            include_properties=True,
            include_direct_children=True,
        ),
    ).sync(client)

    # --- GetFolderResponse level ---
    debug_prop(res.id)
    debug_prop(res.type)
    debug_prop(res.status)
    debug_prop(res.title)
    debug_prop(res.parentId)
    debug_prop(res.parentType)
    debug_prop(res.position)
    debug_prop(res.authorId)
    debug_prop(res.ownerId)
    debug_prop(res.createdAt)
    debug_prop(res.spaceId)
    debug_prop(res.version)
    debug_prop(res.operations)
    debug_prop(res.properties)
    debug_prop(res.directChildren)
    debug_prop(res.links)

    # --- GetFolderResponseVersion level ---
    debug_prop(res.version.createdAt)
    debug_prop(res.version.message)
    debug_prop(res.version.number)
    debug_prop(res.version.minorEdit)
    debug_prop(res.version.authorId)

    # --- GetFolderResponseLinks level ---
    debug_prop(res.links.webui)

    # --- GetFolderResponseOperations level ---
    debug_prop(res.operations.results)
    debug_prop(res.operations.meta)
    debug_prop(res.operations.links)

    # --- GetFolderResponseOperationsMeta level ---
    debug_prop(res.operations.meta.hasMore)
    debug_prop(res.operations.meta.cursor)

    # --- GetFolderResponseOperation level ---
    if res.operations.results:
        op = res.operations.results[0]
        debug_prop(op.operation)
        debug_prop(op.targetType)

    # --- GetFolderResponseProperties level ---
    debug_prop(res.properties.results)
    debug_prop(res.properties.meta)
    debug_prop(res.properties.links)

    # --- GetFolderResponsePropertiesMeta level ---
    debug_prop(res.properties.meta.hasMore)
    debug_prop(res.properties.meta.cursor)

    # --- GetFolderResponseProperty level ---
    # Note: properties.results may be empty
    # if res.properties.results:
    #     prop = res.properties.results[0]
    #     debug_prop(prop.id)
    #     debug_prop(prop.key)
    #     debug_prop(prop.value)
    #     debug_prop(prop.version)

    # --- GetFolderResponseDirectChildren level ---
    debug_prop(res.directChildren.results)
    debug_prop(res.directChildren.meta)
    debug_prop(res.directChildren.links)

    # --- GetFolderResponseDirectChildrenMeta level ---
    debug_prop(res.directChildren.meta.hasMore)
    debug_prop(res.directChildren.meta.cursor)

    # --- GetFolderResponseChild level ---
    # Note: directChildren.results may be empty
    # if res.directChildren.results:
    #     child = res.directChildren.results[0]
    #     debug_prop(child.id)
    #     debug_prop(child.status)
    #     debug_prop(child.title)
    #     debug_prop(child.type)
    #     debug_prop(child.spaceId)
    #     debug_prop(child.childPosition)


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.folder.get_folder",
        preview=False,
    )
