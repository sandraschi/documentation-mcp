"""
MCP Bridge - Fleet-wide bridge helper (FastMCP 3.2 create_proxy).

Usage (single-file, no deps beyond fastmcp):
    from mcp_bridge import setup_mcp_bridge, add_bridge_to_capabilities

    bridges = setup_mcp_bridge(mcp, logger)
    # ... in capabilities endpoint:
    caps["features"]["mcp_bridge"] = add_bridge_to_capabilities(bridges)

Env var: MCP_BRIDGE_URLS - comma-separated list of SSE URLs to proxy.
"""

import logging
import os
from typing import Any

try:
    from fastmcp.server import create_proxy
    _HAS_PROXY = True
except ImportError:
    create_proxy = None
    _HAS_PROXY = False


def setup_mcp_bridge(
    mcp: "FastMCP",
    logger: logging.Logger | None = None,
) -> list[str]:
    """
    Configure MCP bridge proxies from MCP_BRIDGE_URLS env var using create_proxy.

    Returns a list of successfully connected bridge URLs (may be empty).
    Gracefully degrades if create_proxy is unavailable or URLs are unset.
    """
    bridges: list[str] = []
    if not _HAS_PROXY:
        if logger:
            logger.warning("create_proxy unavailable - MCP bridge skipped")
        return bridges

    raw = os.getenv("MCP_BRIDGE_URLS", "")
    if not raw:
        return bridges

    for url in raw.split(","):
        url = url.strip()
        if not url:
            continue
        try:
            proxy = create_proxy(url)
            mcp.add_provider(proxy)
            bridges.append(url)
            if logger:
                logger.info("MCP bridge added: %s", url)
        except Exception as e:
            if logger:
                logger.warning("MCP bridge failed for %s: %s", url, e)

    return bridges


def add_bridge_to_capabilities(bridges: list[str]) -> dict[str, Any]:
    """Return the capabilities fragment to merge into /api/capabilities."""
    return {
        "enabled": len(bridges) > 0,
        "bridges": bridges,
        "env_var": "MCP_BRIDGE_URLS",
    }


def probe_bridges(bridges: list[str], logger: logging.Logger | None = None) -> None:
    """Verify each bridge endpoint is reachable. Call during lifespan startup."""
    for url in bridges:
        try:
            import httpx

            resp = httpx.get(url, timeout=5.0)
            resp.raise_for_status()
            if logger:
                logger.info("Bridge probe OK: %s", url)
        except Exception as e:
            if logger:
                logger.warning("Bridge probe failed for %s: %s", url, e)
