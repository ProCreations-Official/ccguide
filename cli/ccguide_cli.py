#!/usr/bin/env python3
"""
CCGuide CLI - Command Line Interface for managing CCGuide

Easy enable/disable functionality for CCGuide without modifying Claude Code settings.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Optional


class CCGuideCLI:
    """CLI interface for CCGuide management."""
    
    def __init__(self):
        self.config_dir = Path.home() / '.ccguide'
        self.config_file = self.config_dir / 'config.json'
        self.status_file = self.config_dir / 'status.json'
        self.ccguide_dir = Path(__file__).parent.parent.absolute()
        
    def print_banner(self):
        """Print CCGuide CLI banner."""
        banner = """
    ╔═══════════════════════════════════════╗
    ║           🧭 CCGuide CLI              ║
    ║     Claude Code AI Guide Manager     ║
    ╚═══════════════════════════════════════╝
        """
        print(banner)
    
    def load_config(self) -> dict:
        """Load CCGuide configuration."""
        if not self.config_file.exists():
            print(f"❌ Config file not found: {self.config_file}")
            print("   Run 'python3 setup.py' first to initialize CCGuide")
            sys.exit(1)
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Failed to load config: {e}")
            sys.exit(1)
    
    def save_config(self, config: dict):
        """Save CCGuide configuration."""
        try:
            self.config_dir.mkdir(exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"❌ Failed to save config: {e}")
            sys.exit(1)
    
    def get_status(self) -> dict:
        """Get current CCGuide status."""
        config = self.load_config()
        
        status = {
            'enabled': config.get('enable_suggestions', False),
            'api_key_set': bool(config.get('gemini_api_key', '').strip()),
            'config_file': str(self.config_file),
            'last_modified': self.config_file.stat().st_mtime if self.config_file.exists() else None
        }
        
        return status
    
    def enable(self):
        """Enable CCGuide suggestions."""
        config = self.load_config()
        
        if config.get('enable_suggestions', False):
            print("✅ CCGuide is already enabled")
            return
        
        config['enable_suggestions'] = True
        self.save_config(config)
        
        print("✅ CCGuide enabled successfully!")
        print("   Suggestions will now be provided after Claude Code sessions")
        
        # Check if API key is set
        if not config.get('gemini_api_key', '').strip():
            print("⚠️  Warning: Gemini API key not configured")
            print("   Set your API key with: ccguide config --api-key YOUR_KEY")
    
    def disable(self):
        """Disable CCGuide suggestions."""
        config = self.load_config()
        
        if not config.get('enable_suggestions', True):
            print("✅ CCGuide is already disabled")
            return
        
        config['enable_suggestions'] = False
        self.save_config(config)
        
        print("✅ CCGuide disabled successfully!")
        print("   No suggestions will be provided until re-enabled")
    
    def toggle(self):
        """Toggle CCGuide on/off."""
        config = self.load_config()
        current_state = config.get('enable_suggestions', True)
        
        if current_state:
            self.disable()
        else:
            self.enable()
    
    def status(self, verbose: bool = False):
        """Show current CCGuide status."""
        try:
            status = self.get_status()
            
            print("📊 CCGuide Status")
            print("=" * 40)
            
            # Main status
            if status['enabled']:
                print("🟢 Status: ENABLED")
                print("   CCGuide will provide suggestions after Claude Code sessions")
            else:
                print("🔴 Status: DISABLED")
                print("   CCGuide will not provide suggestions")
            
            print()
            
            # API Key status
            if status['api_key_set']:
                print("🔑 API Key: SET")
            else:
                print("❌ API Key: NOT SET")
                print("   Configure with: ccguide config --api-key YOUR_KEY")
            
            print()
            
            if verbose:
                print("📁 Configuration:")
                print(f"   Config file: {status['config_file']}")
                print(f"   CCGuide directory: {self.ccguide_dir}")
                
                if status['last_modified']:
                    import datetime
                    mod_time = datetime.datetime.fromtimestamp(status['last_modified'])
                    print(f"   Last modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        except Exception as e:
            print(f"❌ Failed to get status: {e}")
    
    def configure(self, api_key: Optional[str] = None, cooldown: Optional[int] = None, 
                  min_length: Optional[int] = None):
        """Configure CCGuide settings."""
        config = self.load_config()
        changes_made = False
        
        if api_key is not None:
            if api_key.strip():
                config['gemini_api_key'] = api_key.strip()
                print("✅ API key updated")
                changes_made = True
            else:
                print("❌ Invalid API key provided")
        
        if cooldown is not None:
            if cooldown >= 0:
                config['suggestion_cooldown'] = cooldown
                print(f"✅ Cooldown set to {cooldown} seconds")
                changes_made = True
            else:
                print("❌ Cooldown must be >= 0")
        
        if min_length is not None:
            if min_length >= 0:
                config['min_session_length'] = min_length
                print(f"✅ Minimum session length set to {min_length} characters")
                changes_made = True
            else:
                print("❌ Minimum session length must be >= 0")
        
        if changes_made:
            self.save_config(config)
            print("✅ Configuration saved successfully")
        else:
            print("⚠️  No changes made")
    
    def logs(self, lines: int = 20):
        """Show recent CCGuide logs."""
        log_file = self.config_dir / 'assistant.log'
        
        if not log_file.exists():
            print("📋 No logs found")
            print(f"   Log file: {log_file}")
            return
        
        try:
            with open(log_file, 'r') as f:
                log_lines = f.readlines()
            
            print(f"📋 Last {min(lines, len(log_lines))} log entries:")
            print("=" * 60)
            
            for line in log_lines[-lines:]:
                print(line.rstrip())
        
        except Exception as e:
            print(f"❌ Failed to read logs: {e}")
    
    def test(self):
        """Test CCGuide functionality."""
        print("🧪 Testing CCGuide...")
        
        # Check configuration
        try:
            config = self.load_config()
            print("✅ Configuration loaded successfully")
        except:
            print("❌ Configuration loading failed")
            return
        
        # Check if enabled
        if not config.get('enable_suggestions', False):
            print("⚠️  CCGuide is currently disabled")
            print("   Enable with: ccguide enable")
        else:
            print("✅ CCGuide is enabled")
        
        # Check API key
        if not config.get('gemini_api_key', '').strip():
            print("❌ Gemini API key not configured")
            return
        else:
            print("✅ Gemini API key configured")
        
        # Test imports
        try:
            sys.path.insert(0, str(self.ccguide_dir / 'src'))
            from stop_hook_handler import CCGuide
            print("✅ CCGuide modules importable")
        except Exception as e:
            print(f"❌ Module import failed: {e}")
            return
        
        print("🎉 CCGuide appears to be working correctly!")
    
    def hooks_config(self):
        """Generate Claude Code hooks configuration."""
        print("🪝 Claude Code Hooks Configuration")
        print("=" * 50)
        
        hooks_config = {
            "hooks": {
                "Stop": [
                    {
                        "hooks": [
                            {
                                "type": "command",
                                "command": f"python3 {self.ccguide_dir / 'src' / 'stop_hook_handler.py'}",
                                "env": {
                                    "PYTHONPATH": str(self.ccguide_dir)
                                }
                            }
                        ]
                    }
                ]
            }
        }
        
        print("Copy this JSON to your Claude Code settings:")
        print()
        print(json.dumps(hooks_config, indent=2))
        print()
        print("📋 Instructions:")
        print("1. Copy the JSON above")
        print("2. Open your Claude Code settings")
        print("3. Add the hooks configuration")
        print("4. Save and restart Claude Code")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='CCGuide CLI - Manage Claude Code AI Guide',
        prog='ccguide'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show CCGuide status')
    status_parser.add_argument('-v', '--verbose', action='store_true', 
                              help='Show detailed status information')
    
    # Enable command
    subparsers.add_parser('enable', help='Enable CCGuide suggestions')
    
    # Disable command
    subparsers.add_parser('disable', help='Disable CCGuide suggestions')
    
    # Toggle command
    subparsers.add_parser('toggle', help='Toggle CCGuide on/off')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Configure CCGuide settings')
    config_parser.add_argument('--api-key', help='Set Gemini API key')
    config_parser.add_argument('--cooldown', type=int, help='Set suggestion cooldown in seconds')
    config_parser.add_argument('--min-length', type=int, help='Set minimum session length')
    
    # Logs command
    logs_parser = subparsers.add_parser('logs', help='Show recent logs')
    logs_parser.add_argument('-n', '--lines', type=int, default=20, 
                           help='Number of log lines to show (default: 20)')
    
    # Test command
    subparsers.add_parser('test', help='Test CCGuide functionality')
    
    # Hooks command
    subparsers.add_parser('hooks', help='Generate Claude Code hooks configuration')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = CCGuideCLI()
    
    # Handle commands
    if args.command == 'status':
        cli.print_banner()
        cli.status(verbose=args.verbose)
    elif args.command == 'enable':
        cli.enable()
    elif args.command == 'disable':
        cli.disable()
    elif args.command == 'toggle':
        cli.toggle()
    elif args.command == 'config':
        cli.configure(
            api_key=args.api_key,
            cooldown=args.cooldown,
            min_length=args.min_length
        )
    elif args.command == 'logs':
        cli.logs(lines=args.lines)
    elif args.command == 'test':
        cli.print_banner()
        cli.test()
    elif args.command == 'hooks':
        cli.hooks_config()


if __name__ == "__main__":
    main()