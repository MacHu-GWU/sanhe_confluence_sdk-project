# -*- coding: utf-8 -*-

from sanhe_confluence_sdk.tests import client, debug_prop
from sanhe_confluence_sdk.methods.space.get_spaces import GetSpacesRequest, GetSpacesResponse
from sanhe_confluence_sdk.pagi import paginate
from rich import print as rprint

request = GetSpacesRequest()

response: GetSpacesResponse
for response in paginate(
    client=client,
    request=request,
    response_type=GetSpacesResponse,
    page_size=10,
    max_items=35,
):
    # rprint(response.raw_data)
    print(len(response.results))

