# -*- coding: utf-8 -*-

import dataclasses

from .client import Confluence
from .methods.model import (
    BaseRequest,
    BaseResponse,
    T_REQUEST,
    T_RESPONSE,
)
from .methods.common.links import Links
from rich import print as rprint


def paginate(
    client: Confluence,
    request: T_REQUEST,
    response_type: type[T_RESPONSE],
    page_size: int,
    max_items: int,
    limit_field: str = "limit",
    results_field: str = "results",
):
    n_fetched_items = 0
    request = dataclasses.replace(
        request,
        query_params=dataclasses.replace(
            request.query_params,
            **{limit_field: page_size},
        ),
    )
    # print(request) # for debug only
    response = request.sync(client) # paginator only use sync request
    # print(response) # for debug only
    yield response

    while 1:
        n_fetched_items += len(response.raw_data.get(results_field, []))
        if n_fetched_items >= max_items:
            break

        links: Links = response.links
        # links.next could be either NA or a str
        if isinstance(links.next, str) is False:
            break

        url = client.url + links.next
        # print(url) # for debug only
        http_res = client.sync_client.get(url=url)
        response = response_type.from_success_http_response(http_res)
        # print(response) # for debug only
        yield response
