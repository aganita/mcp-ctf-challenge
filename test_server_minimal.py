#!/usr/bin/env python3
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, ListToolsResult

# Create a minimal server
server = Server("test-server")

# Register list_tools handler
@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
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
    result = ListToolsResult(tools=tools)
    print(f"Returning: {result}", file=sys.stderr)
    print(f"Type: {type(result)}", file=sys.stderr)
    return result

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