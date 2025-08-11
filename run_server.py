#!/usr/bin/env python3
"""
Simple startup script for the MCP CTF Challenge Server
This script handles the import path issues and starts the server correctly.
"""

import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# Change to src directory for proper imports
os.chdir(src_dir)

# Now import and run the main module
if __name__ == "__main__":
    try:
        # Import and run the main module's asyncio loop
        import main
        import asyncio
        
        # Create server instance
        mcp_server = main.MCPCTFServer()
        
        # Run the stdio server
        async def run_server():
            try:
                async with main.stdio_server() as (read_stream, write_stream):
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
        
        # Run the async event loop
        asyncio.run(run_server())
        
    except ImportError as e:
        print(f"Import error: {e}", file=sys.stderr)
        print("Make sure you're running this from the project root directory.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)