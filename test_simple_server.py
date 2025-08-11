#!/usr/bin/env python3
"""Simple test server to verify MCP behavior"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Create server
server = Server("test-server")

# Register a simple tool
@server.list_tools()
async def handle_list_tools():
    return [
        Tool(
            name="test_tool",
            description="A simple test tool",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                },
                "required": ["message"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    # Return a list of content items
    return [
        TextContent(
            type="text",
            text=f"Test tool called with: {arguments.get('message', 'no message')}"
        )
    ]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(
            read_stream,
            write_stream,
            init_options
        )

if __name__ == "__main__":
    asyncio.run(main())