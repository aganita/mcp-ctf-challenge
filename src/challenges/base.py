"""
Base challenge class for MCP CTF challenges
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from mcp.types import Tool, CallToolResult, TextContent


class BaseChallenge(ABC):
    """Abstract base class for all CTF challenges"""
    
    def __init__(self, name: str, description: str, difficulty: str):
        self.name = name
        self.description = description
        self.difficulty = difficulty
        self.tools = []
        self._setup_tools()
    
    @abstractmethod
    def _setup_tools(self):
        """Setup tools for this challenge - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle tool calls for this challenge - must be implemented by subclasses"""
        pass
    
    def get_tools(self) -> List[Tool]:
        """Return list of tools provided by this challenge"""
        return self.tools
    
    def owns_tool(self, tool_name: str) -> bool:
        """Check if this challenge owns the specified tool"""
        return any(tool.name == tool_name for tool in self.tools)
    
    def create_error_result(self, message: str) -> CallToolResult:
        """Helper method to create error results"""
        return CallToolResult(
            content=[TextContent(type="text", text=message)],
            isError=True
        )
    
    def create_success_result(self, message: str) -> CallToolResult:
        """Helper method to create success results"""
        return CallToolResult(
            content=[TextContent(type="text", text=message)],
            isError=False
        )