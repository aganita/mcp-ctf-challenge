#!/usr/bin/env python3
"""Test tool execution to debug the validation error"""

import asyncio
from mcp.types import CallToolResult, TextContent

# Test creating a CallToolResult
try:
    # This is what the error suggests is happening
    result = CallToolResult(
        content=[
            TextContent(
                type="text",
                text="Test response"
            )
        ],
        isError=False
    )
    print("✓ CallToolResult created successfully")
    print(f"Result: {result}")
except Exception as e:
    print(f"✗ Error creating CallToolResult: {e}")

# Test what happens if we return a dict instead
try:
    result_dict = {
        "content": [
            {
                "type": "text",
                "text": "Test response"
            }
        ],
        "isError": False
    }
    print("\n✓ Dict structure created successfully")
    print(f"Dict: {result_dict}")
except Exception as e:
    print(f"\n✗ Error creating dict: {e}")