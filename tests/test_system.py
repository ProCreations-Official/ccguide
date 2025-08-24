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

from stop_hook_handler import CCGuide
from gemini_decision_engine import GeminiDecisionEngine


def create_test_transcript(content: str) -> str:
    """Create a temporary transcript file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(content)
        return f.name


def test_basic_functionality():
    """Test basic system functionality without API calls."""
    print("🧪 Testing basic functionality...")
    
    # Test configuration loading
    try:
        ccguide = CCGuide()
        print("✅ CCGuide initialization successful")
    except ValueError as e:
        if "GEMINI_API_KEY" in str(e):
            print("⚠️  CCGuide initialization requires API key (expected for testing)")
            return True
        else:
            print(f"❌ CCGuide initialization failed: {e}")
            return False
    except Exception as e:
        print(f"❌ Unexpected error in CCGuide initialization: {e}")
        return False
    
    return True


def test_transcript_reading():
    """Test transcript reading functionality."""
    print("\\n📄 Testing transcript reading...")
    
    test_content = """
User: Can you help me create a Python function to calculate factorial?