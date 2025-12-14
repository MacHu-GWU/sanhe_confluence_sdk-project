# -*- coding: utf-8 -*-

import dataclasses
from functools import cached_property

from func_args.api import OPT, T_KWARGS

from ...client import Confluence

from ..model import BaseRequest, BaseResponse, NA


# ------------------------------------------------------------------------------
# Input
# ------------------------------------------------------------------------------
@dataclasses.dataclass(frozen=True)
class GetSpacesRequest(BaseRequest):
    ids: list[int] = dataclasses.field(default=OPT)

    @property
    def _path(self) -> str:
        return f"/spaces"

    @property
    def _params(self):
        return {
            "ids": self.ids,
        }

    def sync(self, client: Confluence):
        http_res = self._sync_get(client=client)
        http_res.raise_for_status()
        return GetSpacesResponse(_raw_data=http_res.json())


# ------------------------------------------------------------------------------
# Output
# ------------------------------------------------------------------------------
@dataclasses.dataclass(frozen=True)
class Links(BaseResponse):
    @cached_property
    def next(self) -> str:
        return self._get("next")

    @cached_property
    def base(self) -> str:
        return self._get("base")


@dataclasses.dataclass(frozen=True)
class GetSpacesResponseResultIcon(BaseResponse):
    @cached_property
    def path(self) -> str:
        return self._get("path")

    @cached_property
    def apiDownloadLink(self) -> int:
        return self._get("apiDownloadLink")


@dataclasses.dataclass(frozen=True)
class GetSpacesResponseResult(BaseResponse):
    @cached_property
    def id(self) -> str:
        return self._get("id")

    @cached_property
    def icon(self) -> GetSpacesResponseResultIcon:
        return self._new(GetSpacesResponseResultIcon, "icon")


@dataclasses.dataclass(frozen=True)
class GetSpacesResponse(BaseResponse):
    @cached_property
    def results(self) -> list["GetSpacesResponseResult"]:
        return self._new_many(GetSpacesResponseResult, "results")

    @cached_property
    def _links(self) -> Links:
        return self._new(Links, "_links")
