# -*- coding: utf-8 -*-

import dataclasses

from httpx import Response
from func_args.api import REQ, OPT

from ...client import Confluence

from ..model import BaseRequest, BaseResponse


# ------------------------------------------------------------------------------
# Input
# ------------------------------------------------------------------------------
@dataclasses.dataclass(frozen=True)
class DeletePageRequest(BaseRequest):
    """
    See: https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/#api-pages-id-delete
    """

    # Path parameters (required)
    id: int = dataclasses.field(default=REQ)

    # Query parameters (optional)
    purge: bool = dataclasses.field(default=OPT)
    draft: bool = dataclasses.field(default=OPT)

    @property
    def _path(self) -> str:
        return f"/pages/{self.id}"

    @property
    def _params(self):
        return {
            "purge": self.purge,
            "draft": self.draft,
        }

    def sync(self, client: Confluence) -> Response:
        """
        Execute the DELETE request.

        Returns the httpx.Response object. A successful deletion returns
        status code 204 (No Content).
        """
        return self._sync_delete(DeletePageResponse, client)


# ------------------------------------------------------------------------------
# Output
# ------------------------------------------------------------------------------
@dataclasses.dataclass(frozen=True)
class DeletePageResponse(BaseResponse):
    """response for deleting a page."""
