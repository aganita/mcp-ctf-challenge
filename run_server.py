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
        import main
        print("MCP CTF Challenge Server started successfully!")
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure you're running this from the project root directory.")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)