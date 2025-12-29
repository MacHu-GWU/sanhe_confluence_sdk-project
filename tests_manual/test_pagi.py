# -*- coding: utf-8 -*-

from sanhe_confluence_sdk.pagi import paginate
from sanhe_confluence_sdk.methods.space.get_spaces import (
    GetSpacesRequest,
    GetSpacesRequestQueryParams,
    GetSpacesResponse,
)

from sanhe_confluence_sdk.tests import client, debug_prop


def test_paginate_case_1(
    mute,
):
    request = GetSpacesRequest()
    page_size = 1
    n_page = 2
    n_total_expected = page_size * n_page
    paginator = paginate(
        client=client,
        request=request,
        response_type=GetSpacesResponse,
        page_size=page_size,
        max_items=n_total_expected,
    )
    n_total = 0
    for ith, response in enumerate(paginator, start=1):
        n_record = len(response.results)
        n_total += n_record
        # print(f"{n_record = }")  # for debug only
    assert ith == n_page
    assert n_total == n_total_expected


def test_paginate_case_2(
    mute,
):
    request = GetSpacesRequest()
    page_size = 250
    n_page = 1000
    n_total_expected = page_size * n_page
    paginator = paginate(
        client=client,
        request=request,
        response_type=GetSpacesResponse,
        page_size=page_size,
        max_items=n_total_expected,
    )
    n_total = 0
    for ith, response in enumerate(paginator, start=1):
        n_record = len(response.results)
        n_total += n_record
        # print(f"{n_record = }")  # for debug only
    assert n_total <= n_total_expected


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_cov_test

    run_cov_test(
        __file__,
        "sanhe_confluence_sdk.pagi",
        preview=False,
    )
