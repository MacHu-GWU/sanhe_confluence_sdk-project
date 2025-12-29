# -*- coding: utf-8 -*-

from sanhe_confluence_sdk.pagi import paginate
from sanhe_confluence_sdk.methods.space.get_spaces import (
    GetSpacesRequest,
    GetSpacesResponse,
)

from sanhe_confluence_sdk.tests import client


def test(
    mute,
):
    request = GetSpacesRequest()
    page_size = 250
    max_item = 9999
    paginator = paginate(
        client=client,
        request=request,
        response_type=GetSpacesResponse,
        page_size=page_size,
        max_items=max_item,
    )
    records = []
    for response in paginator:
        records.extend(response.results)
    for record in sorted(records, key=lambda r: r.name):
        print(f"id = {record.id}, key = {record.key}, name = {record.name}")


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_unit_test

    run_unit_test(__file__)
