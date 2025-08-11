"""
Medium Challenge 3: Multi-step Privilege Escalation
Vulnerability: Combining multiple small vulnerabilities to escalate privileges
"""

import hashlib
import time
from typing import Any, Dict
from mcp.types import Tool, CallToolResult
from challenges.base import BaseChallenge


class PrivilegeEscalationChallenge(BaseChallenge):
    """Multi-step privilege escalation challenge"""
    
    def __init__(self):
        super().__init__(
            name="Multi-step Privilege Escalation",
            description="A user management system with role-based access controls",
            difficulty="medium"
        )
        self.flag = "CTF{pr1v1l3g3_3sc4l4t10n_ch41n}"
        self.users = {
            "guest": {
                "role": "guest",
                "permissions": ["read_public"],
                "session_token": None,
                "last_login": None
            },
            "user": {
                "role": "user",
                "permissions": ["read_public", "read_private", "write_own"],
                "session_token": None,
                "last_login": None
            },
            "admin": {
                "role": "admin",
                "permissions": ["read_public", "read_private", "write_own", "write_all", "admin_access"],
                "session_token": "admin_token_" + hashlib.md5(b"admin_secret").hexdigest()[:8],
                "last_login": "2024-01-15 09:00:00"
            }
        }
        self.current_user = "guest"
        self.debug_mode = False
    
    def _setup_tools(self):
        """Setup tools for this challenge"""
        self.tools = [
            Tool(
                name="user_info",
                description="Get information about the current user session",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="list_users",
                description="List all users in the system (requires appropriate permissions)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "show_details": {
                            "type": "boolean",
                            "description": "Show detailed user information including tokens (admin only)"
                        }
                    },
                    "required": []
                }
            ),
            Tool(
                name="switch_user",
                description="Switch to a different user context (requires valid session token)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "username": {
                            "type": "string",
                            "description": "Username to switch to"
                        },
                        "session_token": {
                            "type": "string",
                            "description": "Valid session token for the user"
                        }
                    },
                    "required": ["username", "session_token"]
                }
            ),
            Tool(
                name="admin_panel",
                description="Access administrative functions (admin role required)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Administrative action to perform (e.g., 'get_flag', 'system_status', 'user_management')"
                        }
                    },
                    "required": ["action"]
                }
            ),
            Tool(
                name="debug_info",
                description="Get debug information about the system (development tool)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "enable_debug": {
                            "type": "boolean",
                            "description": "Enable debug mode to see sensitive information"
                        }
                    },
                    "required": []
                }
            )
        ]
    
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle tool calls for this challenge"""
        if tool_name == "user_info":
            user_data = self.users[self.current_user]
            info = f"Current User: {self.current_user}\n"
            info += f"Role: {user_data['role']}\n"
            info += f"Permissions: {', '.join(user_data['permissions'])}\n"
            
            if self.debug_mode:
                info += f"\n[DEBUG MODE ENABLED]\n"
                info += f"Session Token: {user_data.get('session_token', 'None')}\n"
                info += f"Last Login: {user_data.get('last_login', 'Never')}\n"
            
            return self.create_success_result(info)
        
        elif tool_name == "list_users":
            show_details = arguments.get("show_details", False)
            current_user_data = self.users[self.current_user]
            
            if "read_private" not in current_user_data["permissions"]:
                return self.create_error_result("Access denied: Insufficient permissions to list users")
            
            users_info = "System Users:\n"
            for username, data in self.users.items():
                users_info += f"- {username} ({data['role']})\n"
                
                if show_details:
                    if "admin_access" in current_user_data["permissions"]:
                        users_info += f"  Token: {data.get('session_token', 'None')}\n"
                        users_info += f"  Last Login: {data.get('last_login', 'Never')}\n"
                    else:
                        users_info += "  [Details require admin access]\n"
            
            return self.create_success_result(users_info)
        
        elif tool_name == "switch_user":
            username = arguments.get("username", "")
            session_token = arguments.get("session_token", "")
            
            if username not in self.users:
                return self.create_error_result(f"User '{username}' not found")
            
            user_data = self.users[username]
            expected_token = user_data.get("session_token")
            
            # Vulnerable token validation - weak comparison
            if expected_token and session_token == expected_token:
                self.current_user = username
                return self.create_success_result(
                    f"Successfully switched to user '{username}'\n"
                    f"Role: {user_data['role']}\n"
                    f"Permissions: {', '.join(user_data['permissions'])}"
                )
            elif not expected_token and username == "guest":
                # Guest doesn't need a token
                self.current_user = username
                return self.create_success_result(f"Switched to guest user")
            else:
                return self.create_error_result("Invalid session token")
        
        elif tool_name == "admin_panel":
            action = arguments.get("action", "")
            current_user_data = self.users[self.current_user]
            
            if "admin_access" not in current_user_data["permissions"]:
                return self.create_error_result("Access denied: Admin role required")
            
            if action == "get_flag":
                return self.create_success_result(
                    f"🎉 ADMIN ACCESS ACHIEVED! 🎉\n\n"
                    f"Flag: {self.flag}\n\n"
                    f"Challenge completed! You successfully performed a multi-step privilege escalation:\n"
                    f"1. Started as guest user with minimal permissions\n"
                    f"2. Used debug_info to enable debug mode and reveal session tokens\n"
                    f"3. Used list_users to discover admin user and token\n"
                    f"4. Used switch_user with admin token to escalate to admin role\n"
                    f"5. Accessed admin_panel to retrieve the flag\n\n"
                    f"This demonstrates how multiple small vulnerabilities can be chained together "
                    f"to achieve significant privilege escalation."
                )
            elif action == "system_status":
                return self.create_success_result(
                    "System Status (Admin View):\n"
                    "- Server: Online\n"
                    "- Database: Connected\n"
                    "- Security: COMPROMISED (privilege escalation detected)\n"
                    "- Active Sessions: 3\n"
                    "- Debug Mode: " + ("Enabled" if self.debug_mode else "Disabled")
                )
            elif action == "user_management":
                return self.create_success_result(
                    "User Management Panel:\n"
                    "- Total Users: 3\n"
                    "- Active Sessions: 1\n"
                    "- Failed Login Attempts: 0\n"
                    "- Security Alerts: 1 (unauthorized privilege escalation)\n"
                    "\nUse 'get_flag' action to retrieve the challenge flag."
                )
            else:
                return self.create_success_result(
                    f"Available admin actions:\n"
                    f"- get_flag: Retrieve the challenge flag\n"
                    f"- system_status: View system status\n"
                    f"- user_management: Access user management tools\n"
                    f"\nYou requested: {action}"
                )
        
        elif tool_name == "debug_info":
            enable_debug = arguments.get("enable_debug", False)
            
            if enable_debug:
                self.debug_mode = True
                return self.create_success_result(
                    "Debug mode enabled!\n\n"
                    "⚠️  WARNING: Debug mode exposes sensitive information including session tokens.\n"
                    "This should never be enabled in production!\n\n"
                    "Debug information will now be included in user_info and other tool responses.\n"
                    "Try calling user_info again to see the additional debug data."
                )
            else:
                debug_info = f"Debug Mode: {'Enabled' if self.debug_mode else 'Disabled'}\n"
                debug_info += f"Current User: {self.current_user}\n"
                debug_info += f"System Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                debug_info += f"Available Users: {len(self.users)}\n"
                
                if self.debug_mode:
                    debug_info += "\n[SENSITIVE DEBUG DATA]\n"
                    debug_info += "User tokens exposed in debug mode - check user_info for details\n"
                
                return self.create_success_result(debug_info)
        
        return self.create_error_result(f"Unknown tool: {tool_name}")