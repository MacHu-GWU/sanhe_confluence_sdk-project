# -*- coding: utf-8 -*-

from sanhe_confluence_sdk.methods.space.get_space import GetSpaceRequest

from sanhe_confluence_sdk.tests import client, debug_prop, SPACE_ID


def test(
    mute
):
    # Now get the single space by ID with expanded fields
    res = GetSpaceRequest(
        id=SPACE_ID,
        description_format="plain",
        include_icon=True,
        include_labels=True,
        include_properties=True,
        include_operations=True,
        include_permissions=True,
    ).sync(client)

    # --- GetSpaceResponse level ---
    debug_prop(res.id)
    debug_prop(res.key)
    debug_prop(res.name)
    debug_prop(res.type)
    debug_prop(res.status)
    debug_prop(res.authorId)
    debug_prop(res.currentActiveAlias)
    debug_prop(res.createdAt)
    debug_prop(res.homepageId)
    debug_prop(res.description)
    debug_prop(res.icon)
    debug_prop(res.labels)
    debug_prop(res.properties)
    debug_prop(res.operations)
    debug_prop(res.permissions)
    debug_prop(res.roleAssignments)
    debug_prop(res.links)

    # --- GetSpaceResponseDescription level ---
    debug_prop(res.description.plain)
    # debug_prop(res.description.view)  # view is NA when description_format="plain"

    # --- GetSpaceResponseDescriptionPlain level ---
    debug_prop(res.description.plain.representation)
    debug_prop(res.description.plain.value)

    # --- GetSpaceResponseDescriptionView level ---
    # debug_prop(res.description.view.representation)  # view is NA when description_format="plain"
    # debug_prop(res.description.view.value)  # view is NA when description_format="plain"

    # --- GetSpaceResponseIcon level ---
    debug_prop(res.icon.path)
    debug_prop(res.icon.apiDownloadLink)

    # --- GetSpaceResponseLabels level ---
    debug_prop(res.labels.results)
    debug_prop(res.labels.meta)
    debug_prop(res.labels.links)

    # --- GetSpaceResponseLabelsMeta level ---
    debug_prop(res.labels.meta.hasMore)
    debug_prop(res.labels.meta.cursor)

    # --- GetSpaceResponseLabel level ---
    # Note: labels.results may be empty in some spaces
    # if res.labels.results:
    #     label = res.labels.results[0]
    #     debug_prop(label.prefix)
    #     debug_prop(label.name)
    #     debug_prop(label.id)
    #     debug_prop(label.label)

    # --- GetSpaceResponseProperties level ---
    debug_prop(res.properties.results)
    debug_prop(res.properties.meta)
    debug_prop(res.properties.links)

    # --- GetSpaceResponsePropertiesMeta level ---
    debug_prop(res.properties.meta.hasMore)
    debug_prop(res.properties.meta.cursor)

    # --- GetSpaceResponseProperty level ---
    # Note: properties.results may be empty in some spaces
    # if res.properties.results:
    #     prop = res.properties.results[0]
    #     debug_prop(prop.id)
    #     debug_prop(prop.key)
    #     debug_prop(prop.value)
    #     debug_prop(prop.version)

    # --- GetSpaceResponseOperations level ---
    debug_prop(res.operations.results)
    debug_prop(res.operations.meta)
    debug_prop(res.operations.links)

    # --- GetSpaceResponseOperationsMeta level ---
    debug_prop(res.operations.meta.hasMore)
    debug_prop(res.operations.meta.cursor)

    # --- GetSpaceResponseOperation level ---
    op = res.operations.results[0]
    debug_prop(op.operation)
    debug_prop(op.targetType)

    # --- GetSpaceResponsePermissions level ---
    debug_prop(res.permissions.results)
    debug_prop(res.permissions.meta)
    debug_prop(res.permissions.links)

    # --- GetSpaceResponsePermissionsMeta level ---
    debug_prop(res.permissions.meta.hasMore)
    debug_prop(res.permissions.meta.cursor)

    # --- GetSpaceResponsePermission level ---
    perm = res.permissions.results[0]
    debug_prop(perm.id)
    debug_prop(perm.principal)
    debug_prop(perm.operation)

    # --- GetSpaceResponsePermissionSubject level ---
    debug_prop(perm.principal.type)
    debug_prop(perm.principal.identifier)

    # --- GetSpaceResponsePermissionOperation level ---
    debug_prop(perm.operation.key)
    debug_prop(perm.operation.targetType)

    # --- GetSpaceResponseRoleAssignments level ---
    # Note: roleAssignments requires RBAC Early Access Program
    # debug_prop(res.roleAssignments.results)  # roleAssignments is NA if not enrolled in RBAC EAP
    # debug_prop(res.roleAssignments.meta)  # roleAssignments is NA if not enrolled in RBAC EAP

    # --- GetSpaceResponseLinks level ---
    debug_prop(res.links.webui)


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.space.get_space",
        preview=False,
    )
