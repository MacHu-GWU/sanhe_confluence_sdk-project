# -*- coding: utf-8 -*-

"""
Manual test for CreateSpaceRequest API method.

Note: This test creates a real space in Confluence, so it should be run
manually and the space should be deleted afterwards.

IMPORTANT: For POST/PATCH/DELETE (write) requests, ALL test code must be
commented out to prevent accidental damage to real Confluence data.
"""

from sanhe_confluence_sdk.methods.space.create_space import CreateSpaceRequest

from sanhe_confluence_sdk.tests import client, debug_prop


def test(mute):
    """
    Test CreateSpaceRequest API.

    IMPORTANT: This test is fully commented out because it creates real data.
    To run the test:
    1. Uncomment the test code below
    2. Run the test
    3. Delete the created space manually after testing
    4. Re-comment the test code
    """
    # --- Uncomment below to run actual test ---
    # import uuid
    # unique_suffix = uuid.uuid4().hex[:8].upper()
    # space_key = f"TEST{unique_suffix}"
    #
    # res = CreateSpaceRequest(
    #     name=f"Test Space {unique_suffix}",
    #     key=space_key,
    #     description={
    #         "value": "Test space created by sanhe_confluence_sdk",
    #         "representation": "plain",
    #     },
    #     create_private_space=True,
    # ).sync(client)
    #
    # # --- CreateSpaceResponse level ---
    # debug_prop(res.id)
    # debug_prop(res.key)
    # debug_prop(res.name)
    # debug_prop(res.type)
    # debug_prop(res.status)
    # debug_prop(res.authorId)
    # debug_prop(res.currentActiveAlias)
    # debug_prop(res.createdAt)
    # debug_prop(res.homepageId)
    # debug_prop(res.description)
    # debug_prop(res.icon)
    # debug_prop(res.links)
    #
    # # --- CreateSpaceResponseDescription level ---
    # # debug_prop(res.description.plain)  # description may be None
    # # debug_prop(res.description.view)  # description may be None
    #
    # # --- CreateSpaceResponseDescriptionPlain level ---
    # # debug_prop(res.description.plain.representation)  # description may be None
    # # debug_prop(res.description.plain.value)  # description may be None
    #
    # # --- CreateSpaceResponseDescriptionView level ---
    # # debug_prop(res.description.view.representation)  # description may be None
    # # debug_prop(res.description.view.value)  # description may be None
    #
    # # --- CreateSpaceResponseIcon level ---
    # # debug_prop(res.icon.path)  # icon may be None
    # # debug_prop(res.icon.apiDownloadLink)  # icon may be None
    #
    # # --- CreateSpaceResponseLinks level ---
    # debug_prop(res.links.webui)
    #
    # print(f"\nCreated space with key: {space_key}")
    # print(f"Remember to delete the space after testing!")
    pass


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.space.create_space",
        preview=False,
    )
