#!/usr/bin/env python3
"""
MCP HTTP Proxy - Bridges stdio transport to HTTP MCP server
This allows Claude Desktop to connect to remote MCP servers
"""

import sys
import json
import asyncio
import aiohttp
from typing import Any, Dict

class MCPHTTPProxy:
    def __init__(self, server_url: str):
        self.server_url = server_url.rstrip('/')
        self.session = None
    
    async def start(self):
        """Start the proxy"""
        self.session = aiohttp.ClientSession()
        try:
            await self.run_stdio_loop()
        finally:
            await self.session.close()
    
    async def run_stdio_loop(self):
        """Main loop reading from stdin and writing to stdout"""
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        await asyncio.get_event_loop().connect_read_pipe(lambda: protocol, sys.stdin)
        
        writer = sys.stdout
        
        while True:
            try:
                # Read line from stdin
                line = await reader.readline()
                if not line:
                    break
                
                # Parse JSON-RPC request
                request = json.loads(line.decode())
                
                # Forward to HTTP server
                response = await self.forward_request(request)
                
                # Write response to stdout
                writer.write(json.dumps(response).encode() + b'\n')
                writer.flush()
                
            except Exception as e:
                # Send error response
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32603,
                        "message": f"Proxy error: {str(e)}"
                    },
                    "id": request.get("id") if 'request' in locals() else None
                }
                writer.write(json.dumps(error_response).encode() + b'\n')
                writer.flush()
    
    async def forward_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Forward request to HTTP server"""
        async with self.session.post(
            f"{self.server_url}/mcp",
            json=request,
            headers={"Content-Type": "application/json"}
        ) as response:
            return await response.json()

async def main():
    if len(sys.argv) < 2:
        print("Usage: mcp_http_proxy.py <server_url>", file=sys.stderr)
        sys.exit(1)
    
    server_url = sys.argv[1]
    proxy = MCPHTTPProxy(server_url)
    await proxy.start()

if __name__ == "__main__":
    # Run with unbuffered output
    sys.stdout = sys.stdout.detach()
    sys.stdout = open(sys.stdout.fileno(), 'wb', 0)
    
    asyncio.run(main())