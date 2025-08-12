#!/usr/bin/env python3
"""
Test script for HTTP-to-MCP bridge
Run this to verify the remote MCP server is working correctly
"""

import requests
import json
import sys

def test_mcp_server(base_url):
    """Test the MCP server endpoints"""
    
    print(f"Testing MCP server at: {base_url}")
    print("-" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health check endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    # Test 2: List challenges
    print("\n2. Testing challenges endpoint...")
    try:
        response = requests.get(f"{base_url}/challenges")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Found {len(data)} challenges:")
        for name, info in data.items():
            print(f"  - {name}: {info['name']} ({info['difficulty']})")
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    # Test 3: MCP Initialize
    print("\n3. Testing MCP initialize...")
    try:
        payload = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {},
            "id": 1
        }
        response = requests.post(
            f"{base_url}/mcp",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    # Test 4: List tools
    print("\n4. Testing MCP tools/list...")
    try:
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "params": {},
            "id": 2
        }
        response = requests.post(
            f"{base_url}/mcp",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        if "result" in data and "tools" in data["result"]:
            tools = data["result"]["tools"]
            print(f"Found {len(tools)} tools:")
            for tool in tools[:5]:  # Show first 5 tools
                print(f"  - {tool['name']}: {tool['description'][:60]}...")
            if len(tools) > 5:
                print(f"  ... and {len(tools) - 5} more tools")
        else:
            print(f"Response: {json.dumps(data, indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    # Test 5: Call a simple tool
    print("\n5. Testing tool call (ctf_help)...")
    try:
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "ctf_help",
                "arguments": {}
            },
            "id": 3
        }
        response = requests.post(
            f"{base_url}/mcp",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        if "result" in data and "content" in data["result"]:
            content = data["result"]["content"]
            if content and len(content) > 0:
                print(f"Tool response: {content[0]['text'][:200]}...")
        else:
            print(f"Response: {json.dumps(data, indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    print("\n" + "-" * 50)
    print("✅ All tests passed! The MCP server is working correctly.")
    return True

if __name__ == "__main__":
    # Default to localhost, but allow override
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "http://localhost:8000"
    
    # Ensure URL doesn't have trailing slash
    url = url.rstrip("/")
    
    # Run tests
    success = test_mcp_server(url)
    sys.exit(0 if success else 1)