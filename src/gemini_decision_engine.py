"""
Gemini Decision Engine - Uses Flash-Lite for efficient decision making
"""

import time
import logging
from typing import Dict, Any, Optional
from pathlib import Path
import google.generativeai as genai


class GeminiDecisionEngine:
    """Handles decision logic using Gemini 2.5 Flash-Lite for efficiency."""
    
    def __init__(self, api_key: str, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.session_history = {}
        self.cooldown_file = Path.home() / '.ccguide' / 'last_suggestion.txt'
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
    def is_in_cooldown(self, session_id: str) -> bool:
        """Check if we're still in cooldown period for suggestions."""
        cooldown_minutes = self.config.get('suggestion_cooldown', 300) / 60
        
        try:
            if self.cooldown_file.exists():
                last_suggestion_time = float(self.cooldown_file.read_text().strip())
                time_since_last = time.time() - last_suggestion_time
                if time_since_last < self.config.get('suggestion_cooldown', 300):
                    remaining = (self.config.get('suggestion_cooldown', 300) - time_since_last) / 60
                    self.logger.info(f"In cooldown: {remaining:.1f} minutes remaining")
                    return True
        except Exception as e:
            self.logger.warning(f"Failed to check cooldown: {e}")
        
        return False
    
    def update_cooldown(self):
        """Update the last suggestion timestamp."""
        try:
            self.cooldown_file.parent.mkdir(exist_ok=True)
            self.cooldown_file.write_text(str(time.time()))
        except Exception as e:
            self.logger.error(f"Failed to update cooldown: {e}")
    
    def analyze_session_context(self, session_context: str) -> Dict[str, Any]:
        """Analyze session context for decision-making factors."""
        analysis = {
            'length': len(session_context),
            'has_code': any(keyword in session_context.lower() for keyword in 
                          ['def ', 'function', 'class ', 'import ', 'const ', 'var ', 'let ']),
            'has_errors': any(keyword in session_context.lower() for keyword in 
                           ['error', 'exception', 'failed', 'traceback', 'syntax error']),
            'has_testing': any(keyword in session_context.lower() for keyword in 
                            ['test', 'pytest', 'unittest', 'jest', 'spec']),
            'has_git': any(keyword in session_context.lower() for keyword in 
                         ['git ', 'commit', 'branch', 'merge', 'pull request']),
            'complexity_indicators': len([word for word in session_context.split() 
                                        if word.lower() in ['todo', 'fixme', 'hack', 'temp']]),
        }
        
        return analysis
    
    def should_suggest(self, session_id: str, session_context: str) -> bool:
        """Main decision logic using Gemini Flash-Lite."""
        
        # Basic checks first
        if not self.config.get('enable_suggestions', True):
            self.logger.info("Suggestions disabled in config")
            return False
        
        if len(session_context) < self.config.get('min_session_length', 100):
            self.logger.info("Session too short for suggestions")
            return False
        
        if self.is_in_cooldown(session_id):
            return False
        
        # Analyze session context
        analysis = self.analyze_session_context(session_context)
        self.logger.info(f"Session analysis: {analysis}")
        
        # Use full context for AI decision
        full_context = session_context
        
        decision_prompt = f"""
You are a smart filter for Claude Code AI suggestions. Analyze the session and decide if suggestions would be valuable.

SESSION METRICS:
- Length: {analysis['length']} characters
- Has code: {analysis['has_code']}
- Has errors: {analysis['has_errors']}
- Has testing: {analysis['has_testing']}
- Has git activity: {analysis['has_git']}
- Complexity indicators: {analysis['complexity_indicators']}

FULL SESSION CONTEXT:
{full_context}

DECISION CRITERIA:
✅ Suggest if:
- Significant coding work was done
- Code quality issues are apparent
- Security concerns exist
- Testing gaps are visible
- Documentation is missing
- Architecture could be improved
- Best practices weren't followed

❌ Don't suggest if:
- Task is trivial (simple edits, file reads)
- User is just exploring/learning
- Session is primarily conversational
- Work is already high-quality
- Previous suggestions were ignored

Respond with only "YES" or "NO".
"""
        
        try:
            response = self.model.generate_content(decision_prompt)
            decision = response.text.strip().upper()
            
            should_suggest = decision == "YES"
            
            self.logger.info(f"Gemini decision for session {session_id}: {decision} -> {should_suggest}")
            
            if should_suggest:
                self.update_cooldown()
            
            return should_suggest
            
        except Exception as e:
            self.logger.error(f"Gemini decision engine failed: {e}")
            # Fallback to simple heuristics
            return self._fallback_decision(analysis)
    
    def _fallback_decision(self, analysis: Dict[str, Any]) -> bool:
        """Fallback decision logic when Gemini is unavailable."""
        self.logger.info("Using fallback decision logic")
        
        # Simple heuristic: suggest if session has substantial coding activity
        score = 0
        
        if analysis['length'] > 1000:
            score += 1
        if analysis['has_code']:
            score += 2
        if analysis['has_errors']:
            score += 1
        if analysis['complexity_indicators'] > 0:
            score += 1
        
        should_suggest = score >= 3
        
        if should_suggest:
            self.update_cooldown()
        
        self.logger.info(f"Fallback decision score: {score}/5 -> {should_suggest}")
        return should_suggest