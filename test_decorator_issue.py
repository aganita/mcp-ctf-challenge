#!/usr/bin/env python3
"""Test to understand the decorator issue"""

import asyncio
from mcp.server import Server
from mcp.types import CallToolResult, TextContent

# Create a minimal server
server = Server("test-server")

# Test 1: Handler with explicit types
@server.call_tool()
async def handler_with_types(tool_name: str, arguments: dict) -> CallToolResult:
    return CallToolResult(
        content=[TextContent(type="text", text="Test response")],
        isError=False
    )

# Test 2: Handler without return type annotation
@server.call_tool()
async def handler_without_types(tool_name, arguments):
    return CallToolResult(
        content=[TextContent(type="text", text="Test response")],
        isError=False
    )

# Test 3: Handler that returns a dict
@server.call_tool()
async def handler_returns_dict(tool_name: str, arguments: dict):
    return {
        "content": [{"type": "text", "text": "Test response"}],
        "isError": False
    }

print("✓ All handlers registered successfully")

# Let's see what the decorator actually expects
import inspect
print("\nInspecting the decorator:")
print(f"server.call_tool: {server.call_tool}")
print(f"Type: {type(server.call_tool)}")

# Check if we can see the signature it expects
if hasattr(server.call_tool, '__doc__'):
    print(f"Docstring: {server.call_tool.__doc__}")