# -*- coding: utf-8 -*-

from sanhe_confluence_sdk.pagi import paginate
from sanhe_confluence_sdk.methods.page.get_pages import (
    GetPagesRequest,
    GetPagesResponse,
)

from sanhe_confluence_sdk.tests import client


def test(
    mute,
):
    request = GetPagesRequest()
    page_size = 50
    max_item = 100
    paginator = paginate(
        client=client,
        request=request,
        response_type=GetPagesResponse,
        page_size=page_size,
        max_items=max_item,
    )
    response: GetPagesResponse
    for response in paginator:
        for record in response.results:
            print(
                f"page id = {record.id}, "
                f"title = {record.title!r}, "
                f"url = {client.url + '/wiki' + record.links.webui}"
            )


if __name__ == "__main__":
    from sanhe_confluence_sdk.tests import run_unit_test

    run_unit_test(__file__)
