"""
CCGuide Core Modules

This package contains the core functionality for CCGuide:
- stop_hook_handler: Main entry point for Claude Code hooks
- gemini_decision_engine: Intelligent decision making with Flash-Lite
- gemini_suggestion_engine: Contextual suggestions with Flash
"""

__version__ = "1.0.0"
__author__ = "ProCreations Official"

from .stop_hook_handler import CCGuide
from .gemini_decision_engine import GeminiDecisionEngine  
from .gemini_suggestion_engine import GeminiSuggestionEngine

__all__ = [
    "CCGuide",
    "GeminiDecisionEngine", 
    "GeminiSuggestionEngine"
]