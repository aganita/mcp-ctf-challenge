"""
Easy Challenge 3: Excessive File Access
Vulnerability: No path validation, can read any file
"""

import os
from typing import Any, Dict
from mcp.types import Tool, CallToolResult
from challenges.base import BaseChallenge


class FileAccessChallenge(BaseChallenge):
    """Excessive file access permissions challenge"""
    
    def __init__(self):
        super().__init__(
            name="Excessive File Access",
            description="A file reading utility with basic access controls",
            difficulty="easy"
        )
        self.flag = "CTF{f1l3_4cc3ss_v1ol4t10n}"
        self._setup_files()
    
    def _setup_files(self):
        """Create some files for the challenge"""
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Create public files
        with open("data/readme.txt", "w") as f:
            f.write("Welcome to the file system!\n\nAvailable files:\n- readme.txt (this file)\n- help.txt\n- config.txt\n\nUse the read_file tool to access these files.")
        
        with open("data/help.txt", "w") as f:
            f.write("File Access Help\n================\n\nThis system allows you to read certain files.\nOnly files in the data/ directory should be accessible.\n\nSecurity Note: The system should prevent access to sensitive files.")
        
        with open("data/config.txt", "w") as f:
            f.write("# Configuration File\napp_name=FileReader\nversion=1.0\ndebug=false\n\n# Note: Sensitive configuration should be in separate files")
        
        # Create the secret file (this should be protected)
        with open("data/secret.txt", "w") as f:
            f.write(f"CONFIDENTIAL SYSTEM FILE\n\nThis file contains sensitive information and should not be accessible to regular users.\n\nSecret Flag: {self.flag}\n\nAccess to this file indicates a security vulnerability in the file access controls.")
    
    def _setup_tools(self):
        """Setup tools for this challenge"""
        self.tools = [
            Tool(
                name="read_file",
                description="Read the contents of a file. Only files in the data directory should be accessible for security reasons.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "Name of the file to read (e.g., 'readme.txt', 'help.txt')"
                        }
                    },
                    "required": ["filename"]
                }
            ),
            Tool(
                name="list_files",
                description="List available files in the system",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
        ]
    
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle tool calls for this challenge"""
        if tool_name == "read_file":
            filename = arguments.get("filename", "")
            
            # Vulnerable implementation - no proper path validation!
            # This allows path traversal attacks
            try:
                # Weak attempt at security - easily bypassed
                if filename.startswith("/") or ".." in filename:
                    # But we still process it anyway (vulnerability!)
                    pass
                
                # Try to read from data directory first
                file_path = f"data/{filename}"
                if os.path.exists(file_path):
                    with open(file_path, "r") as f:
                        content = f.read()
                    
                    # Check if this is the secret file
                    if "secret.txt" in filename:
                        return self.create_success_result(
                            f"File contents:\n{content}\n\n"
                            f"Challenge completed! You successfully exploited excessive file permissions "
                            f"to access a restricted file. The system failed to properly validate "
                            f"file access permissions, allowing you to read sensitive data."
                        )
                    else:
                        return self.create_success_result(f"File contents:\n{content}")
                
                # If not in data directory, try direct access (major vulnerability!)
                elif os.path.exists(filename):
                    with open(filename, "r") as f:
                        content = f.read()
                    return self.create_success_result(
                        f"File contents:\n{content}\n\n"
                        f"Warning: You accessed a file outside the intended directory structure!"
                    )
                else:
                    return self.create_error_result(f"File not found: {filename}")
                    
            except Exception as e:
                return self.create_error_result(f"Error reading file: {str(e)}")
        
        elif tool_name == "list_files":
            try:
                files = []
                if os.path.exists("data"):
                    for file in os.listdir("data"):
                        if os.path.isfile(f"data/{file}"):
                            files.append(file)
                
                file_list = "\n".join(f"- {file}" for file in files)
                return self.create_success_result(
                    f"Available files in data directory:\n{file_list}\n\n"
                    f"Use read_file with any of these filenames to view their contents."
                )
            except Exception as e:
                return self.create_error_result(f"Error listing files: {str(e)}")
        
        return self.create_error_result(f"Unknown tool: {tool_name}")