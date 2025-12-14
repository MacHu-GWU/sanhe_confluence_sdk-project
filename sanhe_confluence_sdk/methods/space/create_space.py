# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from functools import cached_property

from func_args.api import OPT

from ...client import Confluence

from ..model import BaseRequest, BaseResponse


# ------------------------------------------------------------------------------
# Input
# ------------------------------------------------------------------------------
@dataclasses.dataclass(frozen=True)
class CreateSpaceRequest(BaseRequest):
    """
    See: https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-space/#api-spaces-post
    """

    name: str = dataclasses.field(default=OPT)
    key: str = dataclasses.field(default=OPT)
    alias: str = dataclasses.field(default=OPT)
    description: T.Dict[str, str] = dataclasses.field(default=OPT)
    role_assignments: T.List[T.Dict[str, T.Any]] = dataclasses.field(default=OPT)
    copy_space_access_configuration: int = dataclasses.field(default=OPT)
    create_private_space: bool = dataclasses.field(default=OPT)
    template_key: str = dataclasses.field(default=OPT)

    @property
    def _path(self) -> str:
        return "/spaces"

    @property
    def _body(self):
        return {
            "name": self.name,
            "key": self.key,
            "alias": self.alias,
            "description": self.description,
            "roleAssignments": self.role_assignments,
            "copySpaceAccessConfiguration": self.copy_space_access_configuration,
            "createPrivateSpace": self.create_private_space,
            "templateKey": self.template_key,
        }

    def sync(self, client: Confluence) -> "CreateSpaceResponse":
        return self._sync_post(CreateSpaceResponse, client)


# ------------------------------------------------------------------------------
# Output
# ------------------------------------------------------------------------------
# --- Deepest nested objects first ---
@dataclasses.dataclass(frozen=True)
class CreateSpaceResponseDescriptionPlain(BaseResponse):
    """BodyType schema for plain text representation."""

    @cached_property
    def representation(self) -> str:
        return self._get("representation")

    @cached_property
    def value(self) -> str:
        return self._get("value")


@dataclasses.dataclass(frozen=True)
class CreateSpaceResponseDescriptionView(BaseResponse):
    """BodyType schema for view (HTML) representation."""

    @cached_property
    def representation(self) -> str:
        return self._get("representation")

    @cached_property
    def value(self) -> str:
        return self._get("value")


@dataclasses.dataclass(frozen=True)
class CreateSpaceResponseDescription(BaseResponse):
    """SpaceDescription schema."""

    @cached_property
    def plain(self) -> CreateSpaceResponseDescriptionPlain:
        return self._new(CreateSpaceResponseDescriptionPlain, "plain")

    @cached_property
    def view(self) -> CreateSpaceResponseDescriptionView:
        return self._new(CreateSpaceResponseDescriptionView, "view")


@dataclasses.dataclass(frozen=True)
class CreateSpaceResponseIcon(BaseResponse):
    """SpaceIcon schema."""

    @cached_property
    def path(self) -> str:
        return self._get("path")

    @cached_property
    def apiDownloadLink(self) -> str:
        return self._get("apiDownloadLink")


@dataclasses.dataclass(frozen=True)
class CreateSpaceResponseLinks(BaseResponse):
    """SpaceLinks schema."""

    @cached_property
    def webui(self) -> str:
        return self._get("webui")


# --- Main response object ---
@dataclasses.dataclass(frozen=True)
class CreateSpaceResponse(BaseResponse):
    """SpaceSingle schema - response for creating a space."""

    @cached_property
    def id(self) -> str:
        return self._get("id")

    @cached_property
    def key(self) -> str:
        return self._get("key")

    @cached_property
    def name(self) -> str:
        return self._get("name")

    @cached_property
    def type(self) -> str:
        """SpaceType enum: global, collaboration, knowledge_base, personal, etc."""
        return self._get("type")

    @cached_property
    def status(self) -> str:
        """SpaceStatus enum: current, archived."""
        return self._get("status")

    @cached_property
    def authorId(self) -> str:
        return self._get("authorId")

    @cached_property
    def currentActiveAlias(self) -> str:
        return self._get("currentActiveAlias")

    @cached_property
    def createdAt(self) -> str:
        """ISO 8601 date-time string."""
        return self._get("createdAt")

    @cached_property
    def homepageId(self) -> str:
        return self._get("homepageId")

    @cached_property
    def description(self) -> CreateSpaceResponseDescription:
        return self._new(CreateSpaceResponseDescription, "description")

    @cached_property
    def icon(self) -> CreateSpaceResponseIcon:
        return self._new(CreateSpaceResponseIcon, "icon")

    @cached_property
    def links(self) -> CreateSpaceResponseLinks:
        return self._new(CreateSpaceResponseLinks, "_links")
