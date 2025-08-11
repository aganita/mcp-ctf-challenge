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
        async def handle_list_tools() -> ListToolsResult:
            tools = []
            for challenge_name, challenge in self.challenges.items():
                tools.extend(challenge.get_tools())
            return ListToolsResult(tools=tools)
        
        # Register call_tool handler
        @self.server.call_tool()
        async def handle_call_tool(request: CallToolRequest) -> CallToolResult:
            tool_name = request.params.name
            arguments = request.params.arguments or {}
            
            # Find which challenge owns this tool
            for challenge_name, challenge in self.challenges.items():
                if challenge.owns_tool(tool_name):
                    return await challenge.handle_tool_call(tool_name, arguments)
            
            # Tool not found
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Unknown tool: {tool_name}"
                    )
                ],
                isError=True
            )

if __name__ == "__main__":
    # Create server instance
    mcp_server = MCPCTFServer()
    
    # Check if running on Render (needs HTTP server)
    if os.getenv("RENDER") and FASTAPI_AVAILABLE:
        # Minimal HTTP server for Render deployment
        app = FastAPI(title="MCP CTF Server", version="1.0.0")
        
        @app.get("/")
        async def health_check():
            return {"status": "MCP CTF Server running", "challenges": len(mcp_server.challenges)}
        
        @app.get("/challenges")
        async def list_challenges():
            return {
                name: {
                    "name": challenge.name,
                    "description": challenge.description,
                    "difficulty": challenge.difficulty,
                    "tools": [tool.name for tool in challenge.get_tools()]
                }
                for name, challenge in mcp_server.challenges.items()
            }
        
        # Run HTTP server
        port = int(os.getenv("PORT", 8000))
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        # Local development - use stdio transport
        async def main():
            async with stdio_server() as (read_stream, write_stream):
                await mcp_server.server.run(
                    read_stream,
                    write_stream,
                    InitializationOptions(
                        server_name="mcp-ctf-server",
                        server_version="1.0.0",
                        capabilities=mcp_server.server.get_capabilities()
                    )
                )
        
        asyncio.run(main())