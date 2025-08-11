#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from challenges.easy.prompt_injection import PromptInjectionChallenge
from challenges.easy.tool_poisoning import ToolPoisoningChallenge
from challenges.easy.file_access import FileAccessChallenge
from challenges.easy.token_exposure import TokenExposureChallenge

# Test getting tools from challenges
challenges = {
    "prompt_injection": PromptInjectionChallenge(),
    "tool_poisoning": ToolPoisoningChallenge(),
    "file_access": FileAccessChallenge(),
    "token_exposure": TokenExposureChallenge(),
}

print("Testing tool collection:")
all_tools = []
for name, challenge in challenges.items():
    tools = challenge.get_tools()
    print(f"\n{name}: {len(tools)} tools")
    for tool in tools:
        print(f"  - {tool.name}: {type(tool)}")
    all_tools.extend(tools)

print(f"\nTotal tools collected: {len(all_tools)}")

# Test ListToolsResult
from mcp.types import ListToolsResult

try:
    result = ListToolsResult(tools=all_tools)
    print(f"\nListToolsResult created successfully: {result}")
except Exception as e:
    print(f"\nError creating ListToolsResult: {e}")
    import traceback
    traceback.print_exc()