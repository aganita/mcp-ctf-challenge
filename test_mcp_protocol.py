#!/usr/bin/env python3
import json
import subprocess
import sys

# Test initialize message
initialize_msg = {
    "jsonrpc": "2.0",
    "id": 0,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {
            "name": "test-client",
            "version": "0.1.0"
        }
    }
}

# Start the server
cmd = [
    "/Users/anigma/workspace/claude_code_playground/mcp-ctf-challenge/venv/bin/python",
    "/Users/anigma/workspace/claude_code_playground/mcp-ctf-challenge/run_server.py"
]

proc = subprocess.Popen(
    cmd,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Send initialize message
try:
    proc.stdin.write(json.dumps(initialize_msg) + "\n")
    proc.stdin.flush()
    
    # Wait a bit and then get output
    import time
    time.sleep(2)
    
    proc.terminate()
    stdout, stderr = proc.communicate(timeout=2)
    
    print("Stdout:", stdout)
    print("Stderr:", stderr)
    
except subprocess.TimeoutExpired:
    print("Process timed out")
    proc.terminate()
    stdout, stderr = proc.communicate()
    print("Stdout after timeout:", repr(stdout))
    print("Stderr after timeout:", repr(stderr))
except Exception as e:
    print(f"Error: {e}")
    proc.terminate()