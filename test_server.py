#!/usr/bin/env python3
"""
Simple test script to validate the MCP CTF server implementation
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported correctly"""
    try:
        from challenges.base import BaseChallenge
        print("✓ Base challenge imported successfully")
        
        from challenges.easy.prompt_injection import PromptInjectionChallenge
        from challenges.easy.tool_poisoning import ToolPoisoningChallenge
        from challenges.easy.file_access import FileAccessChallenge
        from challenges.easy.token_exposure import TokenExposureChallenge
        print("✓ Easy challenges imported successfully")
        
        from challenges.medium.indirect_injection import IndirectInjectionChallenge
        from challenges.medium.tool_shadowing import ToolShadowingChallenge
        from challenges.medium.privilege_escalation import PrivilegeEscalationChallenge
        print("✓ Medium challenges imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_challenge_initialization():
    """Test that challenges can be initialized"""
    try:
        from challenges.easy.prompt_injection import PromptInjectionChallenge
        challenge = PromptInjectionChallenge()
        tools = challenge.get_tools()
        print(f"✓ Prompt injection challenge initialized with {len(tools)} tools")
        
        from challenges.medium.privilege_escalation import PrivilegeEscalationChallenge
        challenge = PrivilegeEscalationChallenge()
        tools = challenge.get_tools()
        print(f"✓ Privilege escalation challenge initialized with {len(tools)} tools")
        
        return True
    except Exception as e:
        print(f"✗ Challenge initialization error: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing MCP CTF Server Implementation...")
    print("=" * 50)
    
    success = True
    
    print("\n1. Testing imports...")
    success &= test_imports()
    
    print("\n2. Testing challenge initialization...")
    success &= test_challenge_initialization()
    
    print("\n" + "=" * 50)
    if success:
        print("✓ All tests passed! Server implementation looks good.")
    else:
        print("✗ Some tests failed. Check the errors above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())