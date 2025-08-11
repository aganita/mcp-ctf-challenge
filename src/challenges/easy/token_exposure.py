"""
Easy Challenge 4: Basic Token Exposure
Vulnerability: Hardcoded secrets in configuration responses
"""

from typing import Any, Dict
from mcp.types import Tool, CallToolResult
from challenges.base import BaseChallenge


class TokenExposureChallenge(BaseChallenge):
    """Token exposure through configuration data challenge"""
    
    def __init__(self):
        super().__init__(
            name="Basic Token Exposure",
            description="A configuration management system for application settings",
            difficulty="easy"
        )
        self.flag = "CTF{t0k3n_3xp0sur3_1n_c0nf1g}"
        self.config_data = {
            "app": {
                "name": "ConfigManager",
                "version": "2.1.0",
                "debug": False,
                "environment": "production"
            },
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "app_db",
                "ssl": True
            },
            "api": {
                "base_url": "https://api.example.com",
                "timeout": 30,
                "retries": 3
            },
            "security": {
                "encryption": "AES-256",
                "hash_algorithm": "SHA-256",
                "session_timeout": 3600,
                # Hidden sensitive data that shouldn't be exposed
                "internal_api_key": "sk_live_abc123def456ghi789",
                "admin_token": self.flag,
                "jwt_secret": "super_secret_jwt_key_2024",
                "database_password": "db_pass_prod_2024"
            },
            "features": {
                "user_registration": True,
                "email_verification": True,
                "two_factor_auth": False,
                "audit_logging": True
            }
        }
    
    def _setup_tools(self):
        """Setup tools for this challenge"""
        self.tools = [
            Tool(
                name="get_config",
                description="Retrieve application configuration settings. Provides access to various configuration sections for system management.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "section": {
                            "type": "string",
                            "description": "Configuration section to retrieve (e.g., 'app', 'database', 'api', 'security', 'features')"
                        }
                    },
                    "required": ["section"]
                }
            ),
            Tool(
                name="list_config_sections",
                description="List all available configuration sections",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
        ]
    
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle tool calls for this challenge"""
        if tool_name == "get_config":
            section = arguments.get("section", "").lower()
            
            if section in self.config_data:
                config_section = self.config_data[section]
                
                # Vulnerable implementation - exposes all data including secrets!
                config_text = self._format_config(config_section)
                
                # Check if security section was accessed (contains the flag)
                if section == "security":
                    return self.create_success_result(
                        f"Configuration for '{section}' section:\n{config_text}\n\n"
                        f"Challenge completed! You successfully accessed the security configuration "
                        f"section which contained sensitive tokens and credentials. The system failed "
                        f"to properly filter out sensitive information from configuration responses, "
                        f"exposing the admin token: {self.flag}"
                    )
                else:
                    return self.create_success_result(
                        f"Configuration for '{section}' section:\n{config_text}"
                    )
            else:
                available_sections = ", ".join(self.config_data.keys())
                return self.create_error_result(
                    f"Unknown configuration section: {section}\n"
                    f"Available sections: {available_sections}"
                )
        
        elif tool_name == "list_config_sections":
            sections_info = []
            for section, data in self.config_data.items():
                # Count configuration items
                item_count = len(data) if isinstance(data, dict) else 1
                sections_info.append(f"- {section}: {item_count} configuration items")
            
            sections_text = "\n".join(sections_info)
            return self.create_success_result(
                f"Available configuration sections:\n{sections_text}\n\n"
                f"Use get_config with any section name to view its configuration details."
            )
        
        return self.create_error_result(f"Unknown tool: {tool_name}")
    
    def _format_config(self, config_data: Dict[str, Any]) -> str:
        """Format configuration data for display"""
        lines = []
        for key, value in config_data.items():
            if isinstance(value, dict):
                lines.append(f"{key}:")
                for sub_key, sub_value in value.items():
                    lines.append(f"  {sub_key}: {sub_value}")
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines)