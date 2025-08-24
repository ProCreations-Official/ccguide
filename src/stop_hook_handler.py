#!/usr/bin/env python3
"""
CCGuide - Claude Code AI Guide

This script is triggered by Claude Code's stop hook to provide AI-powered
guidance and suggestions using Google Gemini API.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

import google.generativeai as genai

# Import from same directory
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from gemini_decision_engine import GeminiDecisionEngine
from gemini_suggestion_engine import GeminiSuggestionEngine


class CCGuide:
    """Main handler for CCGuide - Claude Code AI guidance system."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.setup_logging()
        self.config = self.load_config(config_path)
        self.setup_gemini()
    
    def setup_logging(self):
        """Setup logging for debugging and monitoring."""
        log_dir = Path.home() / '.ccguide'
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'assistant.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file or environment."""
        if config_path:
            config_file = Path(config_path)
        else:
            config_file = Path.home() / '.ccguide' / 'config.json'
        
        default_config = {
            'gemini_api_key': os.getenv('GEMINI_API_KEY'),
            'decision_model': 'gemini-2.5-flash-lite',
            'suggestion_model': 'gemini-2.5-flash',
            'enable_suggestions': True,
            'min_session_length': 100,  # Minimum chars before suggesting
            'suggestion_cooldown': 300,  # 5 minutes between suggestions
        }
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
                self.logger.info(f"Loaded config from {config_file}")
            except Exception as e:
                self.logger.warning(f"Failed to load config: {e}, using defaults")
        
        return default_config
    
    def setup_gemini(self):
        """Initialize Gemini API client."""
        api_key = self.config.get('gemini_api_key')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in config or environment")
        
        # Initialize specialized engines
        self.decision_engine = GeminiDecisionEngine(api_key, self.config)
        self.suggestion_engine = GeminiSuggestionEngine(api_key, self.config)
        
        # Keep legacy models for fallback
        genai.configure(api_key=api_key)
        self.decision_model = genai.GenerativeModel(self.config['decision_model'])
        self.suggestion_model = genai.GenerativeModel(self.config['suggestion_model'])
        
        self.logger.info("Gemini API initialized successfully")
    
    def read_transcript(self, transcript_path: str) -> str:
        """Read Claude Code session transcript."""
        try:
            with open(transcript_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.logger.info(f"Read transcript: {len(content)} characters")
            return content
        except Exception as e:
            self.logger.error(f"Failed to read transcript: {e}")
            return ""
    
    def should_provide_suggestion(self, session_context: str) -> bool:
        """Use Gemini Flash-Lite to decide if a suggestion should be provided."""
        if not self.config['enable_suggestions']:
            return False
        
        if len(session_context) < self.config['min_session_length']:
            return False
        
        decision_prompt = f"""
You are an AI assistant analyzing a Claude Code session to determine if helpful suggestions should be provided.

Analyze the following Claude Code session transcript and determine if suggestions would be valuable:

SESSION TRANSCRIPT:
{session_context}

Consider providing suggestions if:
1. There are potential improvements or optimizations
2. Best practices could be applied
3. Security considerations should be addressed
4. Alternative approaches might be better
5. Code quality could be enhanced
6. Testing or documentation gaps exist

Do NOT suggest if:
1. The task is trivial or already optimal
2. The session is too short or incomplete
3. User explicitly declined suggestions
4. Recent suggestions were already provided

Respond with only "YES" or "NO" and nothing else.
"""
        
        try:
            response = self.decision_model.generate_content(decision_prompt)
            decision = response.text.strip().upper()
            
            should_suggest = decision == "YES"
            self.logger.info(f"Decision: {decision} -> {should_suggest}")
            return should_suggest
            
        except Exception as e:
            self.logger.error(f"Decision model failed: {e}")
            return False
    
    def generate_suggestion(self, session_context: str) -> str:
        """Use Gemini Flash to generate detailed suggestions."""
        suggestion_prompt = f"""
You are an expert AI coding assistant providing helpful suggestions for Claude Code sessions.

Analyze the complete session transcript and provide actionable, specific suggestions for improvement.

SESSION TRANSCRIPT:
{session_context}

Provide suggestions in the following areas if relevant:
1. **Code Quality**: Improvements, optimizations, best practices
2. **Security**: Potential vulnerabilities or security enhancements
3. **Testing**: Missing tests, better test coverage, test strategies
4. **Documentation**: Missing docs, better comments, README improvements
5. **Architecture**: Better design patterns, refactoring opportunities
6. **Performance**: Optimization opportunities, efficiency improvements
7. **Maintenance**: Code organization, dependency management

Format your response as:
## 🤖 AI Suggestions

[Your specific, actionable suggestions here]

Keep suggestions:
- Specific and actionable
- Focused on the most impactful improvements
- Relevant to the current codebase and context
- Concise but comprehensive
"""
        
        try:
            response = self.suggestion_model.generate_content(suggestion_prompt)
            suggestion = response.text.strip()
            self.logger.info(f"Generated suggestion: {len(suggestion)} characters")
            return suggestion
            
        except Exception as e:
            self.logger.error(f"Suggestion model failed: {e}")
            return "❌ Failed to generate suggestions. Please check the logs."
    
    def process_stop_hook(self, session_id: str, transcript_path: str) -> Dict[str, Any]:
        """Main handler for Claude Code stop hook."""
        self.logger.info(f"Processing stop hook for session {session_id}")
        
        # Read session transcript
        session_context = self.read_transcript(transcript_path)
        if not session_context:
            return {"block": False}
        
        # Check if we should provide suggestions using advanced decision engine
        if not self.decision_engine.should_suggest(session_id, session_context):
            self.logger.info("No suggestions needed")
            return {"block": False}
        
        # Generate suggestions using advanced suggestion engine
        suggestion = self.suggestion_engine.generate_contextual_suggestions(session_context)
        
        if suggestion:
            # Return suggestions to Claude Code
            return {
                "block": False,
                "context": suggestion,
                "reason": "CCGuide suggestions available"
            }
        else:
            return {"block": False}


def main():
    """Main entry point for the hook handler."""
    try:
        # Parse command line arguments or environment variables
        session_id = os.getenv('SESSION_ID', sys.argv[1] if len(sys.argv) > 1 else 'unknown')
        transcript_path = os.getenv('TRANSCRIPT_PATH', sys.argv[2] if len(sys.argv) > 2 else '')
        
        if not transcript_path:
            print(json.dumps({"block": False, "error": "No transcript path provided"}))
            return
        
        # Initialize and run the assistant
        assistant = CCGuide()
        result = assistant.process_stop_hook(session_id, transcript_path)
        
        # Output result as JSON for Claude Code
        print(json.dumps(result))
        
    except Exception as e:
        error_result = {
            "block": False,
            "error": f"Hook handler failed: {str(e)}"
        }
        print(json.dumps(error_result))
        logging.error(f"Hook handler failed: {e}")


if __name__ == "__main__":
    main()