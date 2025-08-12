#!/usr/bin/env python3
"""
HTTP-to-MCP Bridge for Remote MCP Server
This module provides HTTP endpoints that translate to MCP protocol calls
"""

import json
import asyncio
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPRequest(BaseModel):
    """Base MCP request model"""
    jsonrpc: str = "2.0"
    method: str
    params: Optional[Dict[str, Any]] = {}
    id: Optional[Any] = None

class MCPResponse(BaseModel):
    """Base MCP response model"""
    jsonrpc: str = "2.0"
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[Any] = None

class MCPHTTPBridge:
    """HTTP bridge for MCP protocol"""
    
    def __init__(self, mcp_server):
        self.mcp_server = mcp_server
        self.app = FastAPI(
            title="MCP CTF Server",
            version="1.0.0",
            description="MCP CTF Challenge Server with HTTP transport"
        )
        
        # Add CORS middleware for browser-based clients
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup HTTP routes for MCP protocol"""
        
        @self.app.get("/")
        async def health_check():
            """Health check endpoint"""
            return {
                "message": "MCP CTF Server is running",
                "status": "healthy",
                "protocol": "MCP over HTTP",
                "challenges": len(self.mcp_server.challenges)
            }
        
        @self.app.get("/challenges")
        async def list_challenges():
            """List all available challenges"""
            return {
                name: {
                    "name": challenge.name,
                    "description": challenge.description,
                    "difficulty": challenge.difficulty,
                    "tools": [tool.name for tool in challenge.get_tools()]
                }
                for name, challenge in self.mcp_server.challenges.items()
            }
        
        @self.app.post("/mcp")
        async def handle_mcp_request(request: Request):
            """Main MCP protocol endpoint"""
            try:
                # Parse JSON-RPC request
                body = await request.json()
                mcp_request = MCPRequest(**body)
                
                logger.info(f"MCP Request: {mcp_request.method}")
                
                # Route to appropriate handler
                if mcp_request.method == "initialize":
                    result = await self._handle_initialize(mcp_request.params)
                elif mcp_request.method == "tools/list":
                    result = await self._handle_list_tools()
                elif mcp_request.method == "tools/call":
                    result = await self._handle_call_tool(mcp_request.params)
                else:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Unknown method: {mcp_request.method}"
                    )
                
                # Return JSON-RPC response
                response = MCPResponse(
                    jsonrpc="2.0",
                    result=result,
                    id=mcp_request.id
                )
                
                # Clean up the response - remove None fields
                response_dict = response.dict(exclude_none=True)
                return response_dict
                
            except Exception as e:
                logger.error(f"Error handling MCP request: {e}")
                error_response = MCPResponse(
                    jsonrpc="2.0",
                    error={
                        "code": -32603,
                        "message": str(e)
                    },
                    id=mcp_request.id if 'mcp_request' in locals() else None
                )
                return error_response.dict(exclude_none=True)
        
        @self.app.options("/mcp")
        async def mcp_options():
            """Handle OPTIONS requests for CORS"""
            return Response(status_code=200)
    
    async def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request"""
        return {
            "protocolVersion": "0.1.0",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "mcp-ctf-server",
                "version": "1.0.0"
            }
        }
    
    async def _handle_list_tools(self) -> Dict[str, Any]:
        """Handle tools/list request"""
        tools = []
        for challenge_name, challenge in self.mcp_server.challenges.items():
            for tool in challenge.get_tools():
                tools.append({
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.inputSchema.dict() if tool.inputSchema else {}
                })
        
        return {"tools": tools}
    
    async def _handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if not tool_name:
            raise ValueError("Tool name is required")
        
        # Find which challenge owns this tool
        for challenge_name, challenge in self.mcp_server.challenges.items():
            if challenge.owns_tool(tool_name):
                result = await challenge.handle_tool_call(tool_name, arguments)
                
                # Convert CallToolResult to dict
                if result.isError:
                    raise ValueError(result.content[0].text if result.content else "Tool execution failed")
                
                # Extract content from result
                content_list = []
                for content in result.content:
                    if hasattr(content, 'text'):
                        content_list.append({
                            "type": "text",
                            "text": content.text
                        })
                
                return {
                    "content": content_list
                }
        
        raise ValueError(f"Unknown tool: {tool_name}")