# -*- coding: utf-8 -*-

from sanhe_confluence_sdk.methods.space.get_spaces import GetSpacesRequest

from sanhe_confluence_sdk.tests import client, debug_prop


def test():
    res = GetSpacesRequest().sync(client)
    # debug_prop(res.results)
    result = res.results[0]
    debug_prop(result)
    debug_prop(result.icon)
    # debug_prop(res._links)


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.methods.space.get_spaces",
        preview=False,
    )
