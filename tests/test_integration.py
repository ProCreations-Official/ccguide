#!/usr/bin/env python3
"""
CCGuide Integration Test

Complete test script to verify CCGuide system functionality.
"""

import os
import sys
import json
import tempfile
from pathlib import Path

# Add ccguide to Python path
sys.path.insert(0, str(Path(__file__).parent))


def print_banner():
    """Print test banner."""
    print("="*50)
    print("🧭 CCGuide Integration Test")
    print("="*50)


def test_imports():
    """Test that all modules can be imported."""
    print("\n📦 Testing module imports...")
    
    try:
        from stop_hook_handler import CCGuide
        print("✅ stop_hook_handler imported")
        
        from gemini_decision_engine import GeminiDecisionEngine
        print("✅ gemini_decision_engine imported")
        
        from gemini_suggestion_engine import GeminiSuggestionEngine
        print("✅ gemini_suggestion_engine imported")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_config_loading():
    """Test configuration file loading."""
    print("\n⚙️  Testing configuration loading...")
    
    # Create temporary config
    config_dir = Path.home() / '.ccguide_test'
    config_dir.mkdir(exist_ok=True)
    
    test_config = {
        "gemini_api_key": "test_key_placeholder",
        "enable_suggestions": True,
        "min_session_length": 100,
        "suggestion_cooldown": 300
    }
    
    config_file = config_dir / 'config.json'
    with open(config_file, 'w') as f:
        json.dump(test_config, f, indent=2)
    
    try:
        from stop_hook_handler import CCGuide
        # Test with config path
        ccguide = CCGuide(config_path=str(config_file))
        print("✅ Configuration loading successful")
        
        # Cleanup
        config_file.unlink()
        config_dir.rmdir()
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def test_transcript_processing():
    """Test transcript file processing."""
    print("\n📄 Testing transcript processing...")
    
    sample_transcript = """User: Help me create a Python function for factorial calculation.