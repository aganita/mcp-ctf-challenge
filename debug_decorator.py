#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp.server import Server
from mcp.types import Tool, ListToolsResult

# Create a server
server = Server("debug-server")

# Try different return approaches
@server.list_tools()
async def handle_list_tools():
    tools = [
        Tool(
            name="test_tool",
            description="A test tool",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Test message"
                    }
                },
                "required": ["message"]
            }
        )
    ]
    
    # Try 1: Return ListToolsResult object
    result = ListToolsResult(tools=tools)
    print(f"Created ListToolsResult: {result}", file=sys.stderr)
    print(f"Type: {type(result)}", file=sys.stderr)
    print(f"Tools attr: {result.tools}", file=sys.stderr)
    
    # Check if it has model_dump
    if hasattr(result, 'model_dump'):
        print(f"model_dump: {result.model_dump()}", file=sys.stderr)
    
    return result

# Test the handler directly
import asyncio

async def test():
    result = await handle_list_tools()
    print(f"Direct call result: {result}")
    print(f"Direct call type: {type(result)}")

asyncio.run(test())