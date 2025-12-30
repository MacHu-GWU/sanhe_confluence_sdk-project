# -*- coding: utf-8 -*-

from sanhe_confluence_sdk.pagi import paginate
from sanhe_confluence_sdk.methods.label.get_labels import (
    GetLabelsRequest,
    GetLabelsResponse,
)

from sanhe_confluence_sdk.tests import client


def test(
    mute,
):
    request = GetLabelsRequest()
    page_size = 250
    max_item = 9999
    paginator = paginate(
        client=client,
        request=request,
        response_type=GetLabelsResponse,
        page_size=page_size,
        max_items=max_item,
    )
    records = []
    for response in paginator:
        records.extend(response.results)
    for record in sorted(records, key=lambda r: r.name):
        print(f"label id = {record.id}, name = {record.name}")


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_unit_test

    run_unit_test(__file__)
