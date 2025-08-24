# Contributing to CCGuide

🎉 Thank you for considering contributing to CCGuide! We welcome contributions from everyone and are grateful for every contribution, no matter how small.

## 🚀 Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/ccguide.git
   cd ccguide
   ```
3. **Create a new branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and test them
5. **Submit a pull request**

## 🐛 Bug Reports

When reporting bugs, please include:

- **Clear description** of the issue
- **Steps to reproduce** the problem
- **Expected vs actual behavior**
- **System information** (OS, Python version, etc.)
- **Log output** from `./ccguide logs`
- **Configuration** (anonymize API keys!)

Use this template:

```
**Bug Description**
A clear description of the bug.

**Steps to Reproduce**
1. Run command X
2. See error Y

**Expected Behavior**
What should have happened.

**System Info**
- OS: [e.g., macOS 14.0, Ubuntu 22.04]
- Python: [e.g., 3.11.0]
- CCGuide: [e.g., latest main]

**Logs**
```
./ccguide logs -n 20
```

**Configuration**
```json
{
  "enable_suggestions": true,
  "min_session_length": 100
  // (don't include API key)
}
```
```

## 💡 Feature Requests

We love new ideas! When suggesting features:

- **Describe the problem** you're trying to solve
- **Explain your proposed solution** 
- **Consider alternatives** you've thought of
- **Provide examples** of how it would work

## 🔧 Development Setup

### Prerequisites

- Python 3.8 or higher
- Gemini API key (for testing)
- Git

### Local Development

```bash
# Clone and setup
git clone https://github.com/ProCreations-Official/ccguide.git
cd ccguide

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Run setup
python3 setup.py

# Test the system
./ccguide test
```

### Running Tests

```bash
# Test CLI functionality
./ccguide test

# Test individual components
python3 -c "from stop_hook_handler import CCGuide; print('✅ Imports work')"

# Test with sample data
echo "Sample transcript" > /tmp/test.txt
python3 stop_hook_handler.py test_session /tmp/test.txt
```

## 📝 Code Guidelines

### Python Code Style

- Follow **PEP 8** style guidelines
- Use **type hints** where appropriate
- Add **docstrings** to functions and classes
- Keep functions focused and small
- Use meaningful variable names

### Example:

```python
def analyze_session_context(self, session_context: str) -> Dict[str, Any]:
    """Analyze session context for decision-making factors.
    
    Args:
        session_context: The full Claude Code session transcript
        
    Returns:
        Dictionary containing analysis metrics
    """
    analysis = {
        'length': len(session_context),
        'has_code': self._detect_code(session_context),
        # ...
    }
    return analysis
```

### Git Commit Messages

Use clear, descriptive commit messages:

- **feat:** New feature
- **fix:** Bug fix  
- **docs:** Documentation changes
- **style:** Code style changes
- **refactor:** Code refactoring
- **test:** Adding tests
- **cli:** CLI improvements

Examples:
```
feat: add cooldown configuration option
fix: handle empty transcript files gracefully
docs: update README with new CLI commands
cli: improve status display formatting
```

## 🧪 Testing Your Changes

Before submitting a pull request:

1. **Test basic functionality:**
   ```bash
   ./ccguide test
   ```

2. **Test CLI commands:**
   ```bash
   ./ccguide status
   ./ccguide enable
   ./ccguide disable
   ./ccguide logs -n 5
   ```

3. **Test with sample data:**
   ```bash
   # Create a realistic test transcript
   echo "User: Help me fix this Python function..." > /tmp/test_session.txt
   python3 stop_hook_handler.py test_session /tmp/test_session.txt
   ```

4. **Check for errors in logs:**
   ```bash
   ./ccguide logs -n 20
   ```

## 🎯 Areas for Contribution

We especially welcome contributions in these areas:

### 🔧 Core Functionality
- **Decision Logic**: Improve when CCGuide suggests
- **Suggestion Quality**: Better prompts and context analysis
- **Performance**: Faster processing, reduced API calls
- **Error Handling**: More robust error recovery

### 🧰 CLI & Tools
- **New Commands**: Additional management features
- **Better UX**: Improved status displays, help text
- **Configuration**: More flexible settings management
- **Debugging**: Better diagnostic tools

### 📚 Documentation
- **Tutorials**: Step-by-step guides
- **Examples**: Real-world usage scenarios  
- **API Docs**: Code documentation
- **Troubleshooting**: Common issues and solutions

### 🔌 Integrations
- **Other AI Models**: Support for additional providers
- **IDE Extensions**: Direct IDE integration
- **Monitoring**: Usage analytics and insights
- **Export**: Suggestion history and reporting

### 🧪 Testing
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflows
- **Performance Tests**: Speed and efficiency
- **Security Tests**: Input validation and sanitization

## 📋 Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Update CHANGELOG** if applicable
5. **Reference issues** in your PR description

### PR Template

When you submit a PR, please include:

```
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature  
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (specify)

## Testing
- [ ] Ran `./ccguide test`
- [ ] Tested CLI commands
- [ ] Verified with sample data
- [ ] Checked logs for errors

## Related Issues
Closes #123, Addresses #456
```

## 🏷️ Versioning

We use [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

## 📞 Getting Help

Need help with contributing? 

- **GitHub Issues**: [Create an issue](https://github.com/ProCreations-Official/ccguide/issues)
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check the [README](README.md)

## 🎉 Recognition

All contributors are recognized in our:
- **README contributors section** 
- **Release notes** for major contributions
- **GitHub contributors page**

Thank you for making CCGuide better! 🧭