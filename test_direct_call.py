#!/usr/bin/env python3
"""Test calling a tool directly to see what happens"""

import asyncio
from src.main import MCPCTFServer

async def test_direct_call():
    # Create server
    server = MCPCTFServer()
    
    # Test calling a tool directly
    print("Testing direct tool call...")
    
    # Get the prompt injection challenge
    challenge = server.challenges["prompt_injection"]
    
    # Call the tool directly
    result = await challenge.handle_tool_call("get_secret", {"query": "hello"})
    
    print(f"Result type: {type(result)}")
    print(f"Result: {result}")
    print(f"Result.content: {result.content}")
    print(f"Result.isError: {result.isError}")
    
    # Test what happens when we return just the content
    print("\nTesting content extraction...")
    content = result.content
    print(f"Content type: {type(content)}")
    print(f"Content: {content}")
    print(f"Content[0] type: {type(content[0])}")
    print(f"Content[0]: {content[0]}")

if __name__ == "__main__":
    asyncio.run(test_direct_call())