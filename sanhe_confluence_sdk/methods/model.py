# -*- coding: utf-8 -*-

import typing as T
import json
import dataclasses

from func_args.api import BaseFrozenModel, remove_optional, T_KWARGS, REQ
from func_args.vendor import sentinel
from httpx import Response

from ..client import Confluence

NA = sentinel.create(name="NA")

# TypeVar for generic response class in _sync_get, _new, _new_many
T_Response = T.TypeVar("T_Response", bound="BaseResponse")


@dataclasses.dataclass(frozen=True)
class BaseModel(BaseFrozenModel):
    pass


@dataclasses.dataclass(frozen=True)
class BaseRequest(BaseModel):
    @property
    def _path(self) -> str:
        """
        Returns the API endpoint path relative to the client's root URL.

        For example, if root URL is "https://example.atlassian.net/wiki/api/v2"
        and path is "/spaces", the full URL becomes
        "https://example.atlassian.net/wiki/api/v2/spaces".
        """
        raise NotImplementedError

    @property
    def _params(self) -> T_KWARGS:
        """
        Constructs query parameters from request attributes.

        Subclasses should override this to return attribute-to-parameter mappings.
        The returned dict will be processed by :meth:`_final_params` to remove
        optional/sentinel values before sending.
        """
        return {}

    @property
    def _final_params(self) -> T_KWARGS | None:
        """
        Returns processed query parameters ready for HTTP request.

        Returns None instead of empty dict because httpx.Client.request()
        uses None as the default for params, ensuring consistent behavior
        when no parameters are needed.
        """
        params = remove_optional(**self._params)
        return params if len(params) else None

    @property
    def _body(self) -> T_KWARGS:
        """
        Constructs request body from request attributes.

        Subclasses should override this to return attribute-to-body field mappings
        for POST/PUT/PATCH requests. The returned dict will be processed by
        :meth:`_final_body` to remove optional/sentinel values before sending.
        """
        return {}

    @property
    def _final_body(self) -> T_KWARGS | None:
        """
        Returns processed request body ready for HTTP request.

        Returns None instead of empty dict because httpx.Client.request()
        uses None as the default for json, ensuring consistent behavior
        when no body is needed.
        """
        body = remove_optional(**self._body)
        return body if len(body) else None

    def _sync_get(
        self,
        klass: type[T_Response],
        client: Confluence,
    ) -> T_Response:
        """
        Executes a synchronous GET request to the API endpoint.
        """
        url = f"{client._root_url}{self._path}"
        params = self._final_params
        # --- for debug only
        # print("----- url")
        # print(url)
        # print("----- params")
        # print(json.dumps(params, indent=4))
        http_res = client.sync_client.get(
            url=url,
            params=params,
        )
        http_res.raise_for_status()
        return klass(_raw_data=http_res.json(), _http_res=http_res)

    def _sync_post(
        self,
        klass: type[T_Response],
        client: Confluence,
    ) -> T_Response:
        """
        Executes a synchronous POST request to the API endpoint.
        """
        url = f"{client._root_url}{self._path}"
        params = self._final_params
        body = self._final_body
        # --- for debug only
        # print("----- url")
        # print(url)
        # print("----- params")
        # print(json.dumps(params, indent=4))
        # print("----- body")
        # print(json.dumps(body, indent=4))
        http_res = client.sync_client.post(
            url=url,
            params=params,
            json=body,
        )
        http_res.raise_for_status()
        return klass(_raw_data=http_res.json(), _http_res=http_res)


@dataclasses.dataclass(frozen=True)
class BaseResponse(BaseModel):
    _raw_data: T_KWARGS = dataclasses.field()
    _http_res: Response | None = dataclasses.field(default=None)

    @property
    def raw_data(self):
        """
        Returns the underlying raw JSON data as a read-only accessor.

        The internal ``_raw_data`` attribute uses underscore prefix to indicate
        it should not be modified directly. This property provides safe read
        access while preserving immutability of the response object.
        """
        return self._raw_data

    @property
    def http_res(self) -> Response | None:
        """
        Returns the underlying HTTP response object, if available.

        This allows access to HTTP metadata such as status code and headers.
        """
        return self._http_res

    def _get(self, field: str):
        """
        Gets a simple field value from the raw data.

        We use NA sentinel to indicate "field not present" vs None value.
        """
        return self._raw_data.get(field, NA)

    def _new(self, klass: type[T_Response], field: str):
        """
        Creates a nested response object from a field in the raw data.

        This method handles the three possible states of optional nested objects
        in API responses, allowing callers to distinguish between "field absent"
        vs "field explicitly null" vs "field has data":

        1. Field exists with JSON object → returns new instance of ``klass``
        2. Field exists with None value → returns None (explicit null in API)
        3. Field absent → returns NA sentinel (field not requested/available)
        """
        value = self._raw_data.get(field, NA)
        if value is NA:
            return NA
        elif value is None:
            return value
        else:
            return klass(_raw_data=value)

    def _new_many(self, klass: type[T_Response], field: str):
        """
        Creates a list of nested response objects from an array field.

        This method handles the three possible states of optional array fields
        in API responses, allowing callers to distinguish between "field absent"
        vs "field explicitly null" vs "field has data":

        1. Field exists with list of JSON objects → returns list of ``klass`` instances
        2. Field exists with None value → returns None (explicit null in API)
        3. Field absent → returns NA sentinel (field not requested/available)
        """
        value = self._raw_data.get(field, NA)
        if value is NA:
            return NA
        elif value is None:
            return value
        else:
            return [klass(_raw_data=raw_data) for raw_data in value]
