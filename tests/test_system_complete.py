#!/usr/bin/env python3
"""
CCGuide System Test

Test script to verify CCGuide system integration and functionality.
"""

import os
import sys
import json
import tempfile
from pathlib import Path

# Add ccguide to Python path
sys.path.insert(0, str(Path(__file__).parent))


def create_test_transcript(content: str) -> str:
    """Create a temporary transcript file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(content)
        return f.name


def test_basic_functionality():
    """Test basic system functionality without API calls."""
    print("🧪 Testing basic functionality...")
    
    # Test that modules can be imported
    try:
        from stop_hook_handler import CCGuide
        from gemini_decision_engine import GeminiDecisionEngine
        from gemini_suggestion_engine import GeminiSuggestionEngine
        print("✅ All modules imported successfully")
    except ImportError as e:
        print(f"❌ Module import failed: {e}")
        return False
    
    # Test configuration loading (without API key)
    print("✅ Basic functionality test passed")
    return True


def test_transcript_reading():
    """Test transcript reading functionality."""
    print("\n📄 Testing transcript reading...")
    
    test_content = """
User: Can you help me create a Python function to calculate factorial?