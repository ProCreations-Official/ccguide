"""
Gemini Suggestion Engine - Uses Flash for detailed analysis and suggestions
"""

import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import re
import google.generativeai as genai


class GeminiSuggestionEngine:
    """Handles detailed suggestion generation using Gemini 2.5 Flash."""
    
    def __init__(self, api_key: str, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def analyze_session_components(self, session_context: str) -> Dict[str, Any]:
        """Deep analysis of session components for better suggestions."""
        analysis = {
            'languages': self._detect_languages(session_context),
            'frameworks': self._detect_frameworks(session_context),
            'tools': self._detect_tools(session_context),
            'patterns': self._detect_patterns(session_context),
            'issues': self._detect_potential_issues(session_context),
            'session_type': self._classify_session_type(session_context)
        }
        
        return analysis
    
    def _detect_languages(self, context: str) -> List[str]:
        """Detect programming languages used in the session."""
        language_indicators = {
            'python': ['.py', 'def ', 'import ', 'python', 'pip', 'pytest'],
            'javascript': ['.js', '.ts', '.jsx', '.tsx', 'function', 'const ', 'npm', 'node'],
            'java': ['.java', 'public class', 'import java', 'maven', 'gradle'],
            'c++': ['.cpp', '.h', '#include', 'std::', 'cmake'],
            'rust': ['.rs', 'fn ', 'use ', 'cargo', 'impl '],
            'go': ['.go', 'func ', 'package ', 'import '],
            'html': ['.html', '<html>', '<div>', '<script>'],
            'css': ['.css', 'style', 'display:', 'margin:'],
            'sql': ['.sql', 'SELECT', 'FROM', 'WHERE', 'INSERT'],
            'shell': ['.sh', '#!/bin/bash', 'chmod', 'mkdir']
        }
        
        detected = []
        context_lower = context.lower()
        
        for lang, indicators in language_indicators.items():
            if any(indicator in context_lower for indicator in indicators):
                detected.append(lang)
        
        return detected
    
    def _detect_frameworks(self, context: str) -> List[str]:
        """Detect frameworks and libraries used."""
        framework_indicators = {
            'react': ['react', 'jsx', 'usestate', 'useeffect', 'component'],
            'vue': ['vue', '@click', 'v-model', 'mounted()'],
            'angular': ['angular', '@component', '@injectable', 'ngmodel'],
            'flask': ['flask', 'app.route', '@app.route', 'render_template'],
            'django': ['django', 'models.py', 'views.py', 'urls.py'],
            'express': ['express', 'app.get', 'app.post', 'middleware'],
            'spring': ['spring', '@controller', '@service', '@autowired'],
            'tensorflow': ['tensorflow', 'keras', 'model.fit', 'neural'],
            'pytorch': ['pytorch', 'torch', 'nn.module', 'tensor'],
            'pandas': ['pandas', 'dataframe', 'pd.read', 'groupby'],
            'numpy': ['numpy', 'np.array', 'ndarray', 'matrix'],
        }
        
        detected = []
        context_lower = context.lower()
        
        for framework, indicators in framework_indicators.items():
            if any(indicator in context_lower for indicator in indicators):
                detected.append(framework)
        
        return detected
    
    def _detect_tools(self, context: str) -> List[str]:
        """Detect development tools used."""
        tool_indicators = {
            'git': ['git add', 'git commit', 'git push', 'git pull'],
            'docker': ['docker', 'dockerfile', 'docker-compose'],
            'kubernetes': ['kubectl', 'k8s', 'deployment.yaml'],
            'aws': ['aws', 'ec2', 's3', 'lambda', 'cloudformation'],
            'ci/cd': ['github actions', 'jenkins', 'ci.yml', '.github/workflows'],
            'testing': ['test', 'pytest', 'jest', 'unittest', 'mocha'],
            'linting': ['eslint', 'pylint', 'flake8', 'prettier'],
        }
        
        detected = []
        context_lower = context.lower()
        
        for tool, indicators in tool_indicators.items():
            if any(indicator in context_lower for indicator in indicators):
                detected.append(tool)
        
        return detected
    
    def _detect_patterns(self, context: str) -> List[str]:
        """Detect development patterns and practices."""
        patterns = []
        context_lower = context.lower()
        
        pattern_indicators = {
            'api_development': ['api', 'endpoint', 'rest', 'json', 'request', 'response'],
            'database_work': ['database', 'sql', 'query', 'table', 'migration'],
            'frontend_work': ['frontend', 'ui', 'component', 'styling', 'responsive'],
            'backend_work': ['backend', 'server', 'authentication', 'middleware'],
            'data_analysis': ['data', 'analysis', 'visualization', 'statistics'],
            'machine_learning': ['ml', 'model', 'training', 'prediction', 'algorithm'],
            'devops': ['deployment', 'infrastructure', 'monitoring', 'scaling'],
            'security': ['authentication', 'authorization', 'encryption', 'security'],
        }
        
        for pattern, indicators in pattern_indicators.items():
            if sum(1 for indicator in indicators if indicator in context_lower) >= 2:
                patterns.append(pattern)
        
        return patterns
    
    def _detect_potential_issues(self, context: str) -> List[str]:
        """Detect potential code quality or security issues."""
        issues = []
        context_lower = context.lower()
        
        issue_patterns = {
            'hardcoded_credentials': ['password =', 'api_key =', 'secret =', 'token ='],
            'missing_error_handling': ['except:', 'catch', 'try:'],
            'code_duplication': ['todo', 'fixme', 'hack', 'temporary'],
            'performance_concerns': ['loop', 'nested', 'n+1', 'timeout'],
            'security_concerns': ['eval(', 'exec(', 'shell=true', 'sql injection'],
            'testing_gaps': ['# no tests', 'untested', 'manual testing'],
        }
        
        for issue, indicators in issue_patterns.items():
            if any(indicator in context_lower for indicator in indicators):
                issues.append(issue)
        
        return issues
    
    def _classify_session_type(self, context: str) -> str:
        """Classify the type of development session."""
        context_lower = context.lower()
        
        if any(word in context_lower for word in ['new project', 'initial', 'setup', 'scaffold']):
            return 'project_setup'
        elif any(word in context_lower for word in ['bug', 'fix', 'error', 'debug']):
            return 'bug_fixing'
        elif any(word in context_lower for word in ['feature', 'implement', 'add', 'create']):
            return 'feature_development'
        elif any(word in context_lower for word in ['refactor', 'cleanup', 'optimize', 'improve']):
            return 'refactoring'
        elif any(word in context_lower for word in ['test', 'testing', 'spec', 'coverage']):
            return 'testing'
        elif any(word in context_lower for word in ['deploy', 'release', 'production', 'ci/cd']):
            return 'deployment'
        else:
            return 'general_development'
    
    def generate_contextual_suggestions(self, session_context: str) -> str:
        """Generate context-aware suggestions using Gemini Flash."""
        analysis = self.analyze_session_components(session_context)
        
        # Use full context for AI processing
        context_for_ai = session_context
        
        suggestion_prompt = self._build_suggestion_prompt(context_for_ai, analysis)
        
        try:
            response = self.model.generate_content(suggestion_prompt)
            suggestions = response.text.strip()
            
            self.logger.info(f"Generated {len(suggestions)} chars of suggestions for {analysis['session_type']} session")
            return self._format_suggestions(suggestions, analysis)
            
        except Exception as e:
            self.logger.error(f"Suggestion generation failed: {e}")
            return self._generate_fallback_suggestions(analysis)
    
    def _prepare_context_for_ai(self, context: str, max_chars: int = 15000) -> str:
        """Prepare context for AI processing, focusing on important parts."""
        if len(context) <= max_chars:
            return context
        
        # Take the most recent context but also include the beginning
        beginning = context[:2000]  # First 2000 chars for initial context
        recent = context[-(max_chars-2000):]  # Most recent content
        
        return f"{beginning}\\n\\n... [middle content truncated] ...\\n\\n{recent}"
    
    def _build_suggestion_prompt(self, context: str, analysis: Dict[str, Any]) -> str:
        """Build a comprehensive suggestion prompt based on analysis."""
        return f"""
You are CCGuide, an expert AI assistant providing intelligent coding guidance for Claude Code sessions.

SESSION ANALYSIS:
- Type: {analysis['session_type']}
- Languages: {', '.join(analysis['languages']) if analysis['languages'] else 'None detected'}
- Frameworks: {', '.join(analysis['frameworks']) if analysis['frameworks'] else 'None detected'}
- Tools: {', '.join(analysis['tools']) if analysis['tools'] else 'None detected'}
- Patterns: {', '.join(analysis['patterns']) if analysis['patterns'] else 'None detected'}
- Potential Issues: {', '.join(analysis['issues']) if analysis['issues'] else 'None detected'}

SESSION TRANSCRIPT:
{context}

GUIDANCE REQUEST:
As CCGuide, provide intelligent, actionable suggestions tailored to this specific session. Focus on:

1. **Code Quality & Best Practices** - Specific improvements for the languages/frameworks used
2. **Security Considerations** - Address any security concerns relevant to the work done
3. **Performance Optimization** - Suggest performance improvements where applicable  
4. **Testing Strategy** - Recommend testing approaches for the current work
5. **Documentation & Maintainability** - Suggest documentation improvements
6. **Architecture & Design** - Propose better patterns or architectural improvements
7. **Tooling & Workflow** - Recommend tools or processes that could help

FORMATTING:
Format as markdown with clear sections. Make suggestions:
- Specific to the actual code and context shown
- Actionable with clear next steps
- Prioritized by impact
- Relevant to the session type and detected technologies

Begin with: "## 🧭 CCGuide Suggestions"
"""
    
    def _format_suggestions(self, suggestions: str, analysis: Dict[str, Any]) -> str:
        """Format and enhance the generated suggestions."""
        # Add session context footer
        session_info = f"\\n\\n---\\n*Session Analysis: {analysis['session_type']}*"
        if analysis['languages']:
            session_info += f" *| Languages: {', '.join(analysis['languages'])}*"
        if analysis['frameworks']:
            session_info += f" *| Frameworks: {', '.join(analysis['frameworks'])}*"
        
        return suggestions + session_info
    
    def _generate_fallback_suggestions(self, analysis: Dict[str, Any]) -> str:
        """Generate basic suggestions when AI fails."""
        fallback = "## 🧭 CCGuide Suggestions\\n\\n"
        
        if analysis['session_type'] == 'bug_fixing':
            fallback += "**Bug Fixing Session Detected**\\n"
            fallback += "- Consider adding tests to prevent regression\\n"
            fallback += "- Document the root cause in comments\\n"
            fallback += "- Review error handling around the fix\\n\\n"
        
        elif analysis['session_type'] == 'feature_development':
            fallback += "**Feature Development Session Detected**\\n"
            fallback += "- Write tests before or alongside implementation\\n"
            fallback += "- Consider breaking down large features into smaller components\\n"
            fallback += "- Document new functionality\\n\\n"
        
        else:
            fallback += "**Development Session Detected**\\n"
            fallback += "- Consider adding or updating tests\\n"
            fallback += "- Review code for security best practices\\n"
            fallback += "- Ensure proper error handling\\n\\n"
        
        if analysis['languages']:
            fallback += f"**Technologies Used:** {', '.join(analysis['languages'])}\\n"
        
        fallback += "\\n*CCGuide AI suggestions temporarily unavailable - using fallback guidance*"
        
        return fallback