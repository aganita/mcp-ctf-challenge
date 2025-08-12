#!/usr/bin/env python3
"""
MCP CTF Challenge Server
A vulnerable MCP server designed for educational CTF challenges
"""

import asyncio
import os
from typing import Any, Dict, List
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
)

# Import FastAPI only if needed for deployment
try:
    from fastapi import FastAPI
    import uvicorn
    from mcp_http_bridge import MCPHTTPBridge
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

# Import challenge modules
from challenges.easy.prompt_injection import PromptInjectionChallenge
from challenges.easy.tool_poisoning import ToolPoisoningChallenge
from challenges.easy.file_access import FileAccessChallenge
from challenges.easy.token_exposure import TokenExposureChallenge
from challenges.medium.indirect_injection import IndirectInjectionChallenge
from challenges.medium.tool_shadowing import ToolShadowingChallenge
from challenges.medium.privilege_escalation import PrivilegeEscalationChallenge

class MCPCTFServer:
    """Main MCP CTF Server class"""
    
    def __init__(self):
        self.server = Server("mcp-ctf-server")
        self.challenges = {}
        self._setup_challenges()
        self._register_tools()
    
    def _setup_challenges(self):
        """Initialize all challenge instances"""
        self.challenges = {
            # Easy challenges
            "prompt_injection": PromptInjectionChallenge(),
            "tool_poisoning": ToolPoisoningChallenge(),
            "file_access": FileAccessChallenge(),
            "token_exposure": TokenExposureChallenge(),
            
            # Medium challenges
            "indirect_injection": IndirectInjectionChallenge(),
            "tool_shadowing": ToolShadowingChallenge(),
            "privilege_escalation": PrivilegeEscalationChallenge(),
        }
    
    def _register_tools(self):
        """Register all challenge tools with the MCP server"""
        
        # Register list_tools handler
        @self.server.list_tools()
        async def handle_list_tools():
            tools = []
            for challenge_name, challenge in self.challenges.items():
                tools.extend(challenge.get_tools())
            # Return just the tools list
            return tools
        
        # Register call_tool handler
        @self.server.call_tool()
        async def handle_call_tool(tool_name: str, arguments: Dict[str, Any]):
            # The MCP server decorator expects us to return a list of content items,
            # not a CallToolResult. It will wrap them for us.
            
            # Find which challenge owns this tool
            for challenge_name, challenge in self.challenges.items():
                if challenge.owns_tool(tool_name):
                    result = await challenge.handle_tool_call(tool_name, arguments)
                    # Extract the content from the CallToolResult
                    # If it's an error, we need to raise an exception
                    if result.isError:
                        # Raise exception so the decorator handles it as an error
                        error_text = result.content[0].text if result.content else "Unknown error"
                        raise Exception(error_text)
                    return result.content
            
            # Tool not found - raise exception
            raise Exception(f"Unknown tool: {tool_name}")

if __name__ == "__main__":
    import sys
    try:
        # Create server instance
        mcp_server = MCPCTFServer()
    except Exception as e:
        print(f"Error creating MCP server: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
    
    # Check if running on Render (needs HTTP server)
    if os.getenv("RENDER") and FASTAPI_AVAILABLE:
        # Use HTTP-to-MCP bridge for Render deployment
        bridge = MCPHTTPBridge(mcp_server)
        
        # Run HTTP server with MCP bridge
        port = int(os.getenv("PORT", 8000))
        uvicorn.run(bridge.app, host="0.0.0.0", port=port)
    else:
        # Local development - use stdio transport
        async def main():
            try:
                async with stdio_server() as (read_stream, write_stream):
                    init_options = mcp_server.server.create_initialization_options()
                    await mcp_server.server.run(
                        read_stream,
                        write_stream,
                        init_options
                    )
            except Exception as e:
                print(f"Error in MCP server: {e}", file=sys.stderr)
                import traceback
                traceback.print_exc(file=sys.stderr)
                raise
        
        try:
            asyncio.run(main())
        except Exception as e:
            print(f"Fatal error running MCP server: {e}", file=sys.stderr)
            sys.exit(1)