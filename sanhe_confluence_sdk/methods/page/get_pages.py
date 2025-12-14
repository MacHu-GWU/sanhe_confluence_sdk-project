# -*- coding: utf-8 -*-

import dataclasses
from functools import cached_property

from func_args.api import OPT

from ...client import Confluence

from ..model import BaseRequest, BaseResponse


# ------------------------------------------------------------------------------
# Input
# ------------------------------------------------------------------------------
@dataclasses.dataclass(frozen=True)
class GetPagesRequest(BaseRequest):
    """
    See: https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/#api-pages-get
    """

    id: list[int] = dataclasses.field(default=OPT)
    space_id: list[int] = dataclasses.field(default=OPT)
    sort: str = dataclasses.field(default=OPT)
    status: list[str] = dataclasses.field(default=OPT)
    title: str = dataclasses.field(default=OPT)
    body_format: str = dataclasses.field(default=OPT)
    subtype: str = dataclasses.field(default=OPT)
    cursor: str = dataclasses.field(default=OPT)
    limit: int = dataclasses.field(default=OPT)

    @property
    def _path(self) -> str:
        return "/pages"

    @property
    def _params(self):
        return {
            "id": self.id,
            "space-id": self.space_id,
            "sort": self.sort,
            "status": self.status,
            "title": self.title,
            "body-format": self.body_format,
            "subtype": self.subtype,
            "cursor": self.cursor,
            "limit": self.limit,
        }

    def sync(self, client: Confluence) -> "GetPagesResponse":
        return self._sync_get(GetPagesResponse, client)


# ------------------------------------------------------------------------------
# Output
# ------------------------------------------------------------------------------
# --- Deepest nested objects first ---
@dataclasses.dataclass(frozen=True)
class GetPagesResponseResultBodyStorage(BaseResponse):
    """BodyType schema for storage representation."""

    @cached_property
    def representation(self) -> str:
        return self._get("representation")

    @cached_property
    def value(self) -> str:
        return self._get("value")


@dataclasses.dataclass(frozen=True)
class GetPagesResponseResultBodyAtlasDocFormat(BaseResponse):
    """BodyType schema for atlas_doc_format representation."""

    @cached_property
    def representation(self) -> str:
        return self._get("representation")

    @cached_property
    def value(self) -> str:
        return self._get("value")


@dataclasses.dataclass(frozen=True)
class GetPagesResponseResultBody(BaseResponse):
    """BodyBulk schema - contains fields for each representation type requested."""

    @cached_property
    def storage(self) -> GetPagesResponseResultBodyStorage:
        return self._new(GetPagesResponseResultBodyStorage, "storage")

    @cached_property
    def atlas_doc_format(self) -> GetPagesResponseResultBodyAtlasDocFormat:
        return self._new(GetPagesResponseResultBodyAtlasDocFormat, "atlas_doc_format")


@dataclasses.dataclass(frozen=True)
class GetPagesResponseResultVersion(BaseResponse):
    """Version schema."""

    @cached_property
    def createdAt(self) -> str:
        """Date and time when the version was created. ISO 8601 format."""
        return self._get("createdAt")

    @cached_property
    def message(self) -> str:
        """Message associated with the current version."""
        return self._get("message")

    @cached_property
    def number(self) -> int:
        """The version number."""
        return self._get("number")

    @cached_property
    def minorEdit(self) -> bool:
        """Describes if this version is a minor version."""
        return self._get("minorEdit")

    @cached_property
    def authorId(self) -> str:
        """The account ID of the user who created this version."""
        return self._get("authorId")


@dataclasses.dataclass(frozen=True)
class GetPagesResponseResultLinks(BaseResponse):
    """AbstractPageLinks schema."""

    @cached_property
    def webui(self) -> str:
        """Web UI link of the content."""
        return self._get("webui")

    @cached_property
    def editui(self) -> str:
        """Edit UI link of the content."""
        return self._get("editui")

    @cached_property
    def tinyui(self) -> str:
        """Tiny UI link of the content."""
        return self._get("tinyui")


# --- Main result object ---
@dataclasses.dataclass(frozen=True)
class GetPagesResponseResult(BaseResponse):
    """PageBulk schema - represents a single page in the results array."""

    @cached_property
    def id(self) -> str:
        """ID of the page."""
        return self._get("id")

    @cached_property
    def status(self) -> str:
        """ContentStatus enum: current, draft, archived, historical, trashed, deleted, any."""
        return self._get("status")

    @cached_property
    def title(self) -> str:
        """Title of the page."""
        return self._get("title")

    @cached_property
    def spaceId(self) -> str:
        """ID of the space the page is in."""
        return self._get("spaceId")

    @cached_property
    def parentId(self) -> str:
        """ID of the parent page, or null if there is no parent page."""
        return self._get("parentId")

    @cached_property
    def parentType(self) -> str:
        """ParentContentType enum: page, whiteboard, database, embed, folder."""
        return self._get("parentType")

    @cached_property
    def position(self) -> int:
        """Position of child page within the given parent page tree."""
        return self._get("position")

    @cached_property
    def authorId(self) -> str:
        """The account ID of the user who created this page originally."""
        return self._get("authorId")

    @cached_property
    def ownerId(self) -> str:
        """The account ID of the user who owns this page."""
        return self._get("ownerId")

    @cached_property
    def lastOwnerId(self) -> str:
        """The account ID of the user who owned this page previously, or null."""
        return self._get("lastOwnerId")

    @cached_property
    def subtype(self) -> str:
        """The subtype of the page."""
        return self._get("subtype")

    @cached_property
    def createdAt(self) -> str:
        """Date and time when the page was created. ISO 8601 format."""
        return self._get("createdAt")

    @cached_property
    def version(self) -> GetPagesResponseResultVersion:
        return self._new(GetPagesResponseResultVersion, "version")

    @cached_property
    def body(self) -> GetPagesResponseResultBody:
        return self._new(GetPagesResponseResultBody, "body")

    @cached_property
    def links(self) -> GetPagesResponseResultLinks:
        return self._new(GetPagesResponseResultLinks, "_links")


# --- Top level response objects ---
@dataclasses.dataclass(frozen=True)
class GetPagesResponseLinks(BaseResponse):
    """MultiEntityLinks schema for pagination."""

    @cached_property
    def next(self) -> str:
        """Relative URL for the next set of results using cursor pagination."""
        return self._get("next")

    @cached_property
    def base(self) -> str:
        """Base URL of the Confluence site."""
        return self._get("base")


@dataclasses.dataclass(frozen=True)
class GetPagesResponse(BaseResponse):
    """MultiEntityResult<PageBulk> schema - top level response."""

    @cached_property
    def results(self) -> list[GetPagesResponseResult]:
        return self._new_many(GetPagesResponseResult, "results")

    @cached_property
    def links(self) -> GetPagesResponseLinks:
        return self._new(GetPagesResponseLinks, "_links")
