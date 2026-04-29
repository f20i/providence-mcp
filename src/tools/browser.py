from __future__ import annotations

import os
from typing import Optional
from fastmcp.tools import tool
from pydantic import Field

from ..common.request import request
from ..schema import BrowserSchema, BrowserListSchema, ProfileSchema, BrowserEndpointSchema, BrowserConnectionSchema

def tranform(browser: dict):
    print("tranform", browser)
    browser_id = browser.get("id")
    browser_job = browser.get("browser_job")

    browser_endpoint = None
    if browser_job is not None and browser_job.get("status") == "running":
        status = browser_job.get("status")
        browser_endpoint = BrowserEndpointSchema(
            status=status,
            connection=BrowserConnectionSchema(
                cdp_url=(
                     f"{os.getenv('PROVIDENCE_EDGE_ENDPOINT', 'http://127.0.0.1:8000')}/browser?browser_id={browser_id}" 
                     if status == "running" else None
                )
            ),
        )

    return BrowserSchema(
        id=browser.get("id"),
        name=browser.get("name"),
        description=browser.get("description"),
        profile=ProfileSchema(**browser.get("profile")),
        browser_endpoint=browser_endpoint
    )

class BrowserToolset:
    @tool(description="Get browser with details from Providence")
    def get_browser(
        self,
        browser_id: str = Field(description="The ID of the browser to get")
    ) -> BrowserSchema:
        response = request("GET", f"/v1/browsers/{browser_id}")
        if response["ok"]:
            return tranform(response["data"])
        else:
            raise Exception(response["error"])

    @tool(description="Get browsers with details from Providence")
    def get_browsers(
        self,
        limit: Optional[int] = Field(default=100, ge=1, le=500, description="The number of browsers to get"),
        offset: Optional[int] = Field(default=0, ge=0, description="The offset of the browsers to get")
    ) -> BrowserListSchema:
        response = request("GET", "/v1/browsers", params={"limit": limit, "offset": offset})
        if response["ok"]:
            return BrowserListSchema(items=[tranform(item) for item in response["data"]["items"]], total=response["data"]["total"])
        else:
            raise Exception(response["error"])