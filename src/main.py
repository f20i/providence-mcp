from __future__ import annotations

from fastmcp import FastMCP
from .tools.browser import BrowserToolset
from .tools.profile import ProfileToolset

browser_toolset = BrowserToolset()
profile_toolset = ProfileToolset()

mcp = FastMCP("providence-mcp")

mcp.add_tool(browser_toolset.get_browser)
mcp.add_tool(profile_toolset.get_profile)
mcp.add_tool(browser_toolset.get_browsers)
mcp.add_tool(profile_toolset.get_profiles)

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8022)
