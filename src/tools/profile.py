from __future__ import annotations

from typing import Optional
from fastmcp.tools import tool
from pydantic import Field
from ..common.request import request
from ..schema import ProfileSchema, ProfileListSchema

class ProfileToolset:
    @tool(description="Get profile with details from Providence")
    def get_profile(
        self,
        profile_id: str = Field(description="The ID of the profile to get")
    ) -> ProfileSchema:
        response = request("GET", f"/v1/profiles/{profile_id}")
        if response["ok"]:
            return ProfileSchema(**response["data"])
        else:
            raise Exception(response["error"])

    @tool(description="Get profiles with details from Providence")
    def get_profiles(
        self,
        limit: Optional[int] = Field(default=100, ge=1, le=500, description="The number of browsers to get"),
        offset: Optional[int] = Field(default=0, ge=0, description="The offset of the browsers to get")
    ) -> ProfileListSchema:
        response = request("GET", "/v1/profiles", params={"limit": limit, "offset": offset})
        if response["ok"]:
            return ProfileListSchema(**response["data"])
        else:
            raise Exception(response["error"])