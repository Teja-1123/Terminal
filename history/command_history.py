import os
from typing import List

class EnhancedCommandHistory:
    """Persistent command history with suggestions"""
    
    def __init__(self, history_file: str = ".terminal_history"):
        self.history_file = os.path.expanduser(f"~/{history_file}")
        self.commands = []
        self.load_history()
    
    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                self.commands = [line.strip() for line in f.readlines()]
    
    def save_history(self):
        with open(self.history_file, 'w') as f:
            for cmd in self.commands[-1000:]:
                f.write(f"{cmd}\n")
    
    def add_command(self, command: str):
        if command.strip() and (not self.commands or self.commands[-1] != command):
            self.commands.append(command)
            self.save_history()
    
    def search_history(self, query: str) -> List[str]:
        return [cmd for cmd in self.commands if query.lower() in cmd.lower()]
    
    def get_suggestions(self, partial_command: str) -> List[str]:
        suggestions = []
        for cmd in reversed(self.commands):
            if cmd.startswith(partial_command) and cmd not in suggestions:
                suggestions.append(cmd)
            if len(suggestions) >= 5:
                break
        return suggestions
    def cmd_history(self, args):
        """Show or search command history"""
        if args and args[0] == 'search':
            if len(args) > 1:
                query = ' '.join(args[1:])
                results = self.command_history.search_history(query)
                print(f"🔹 History search results for '{query}':")
                for i, cmd in enumerate(results, 1):
                    print(f"{i:4} {cmd}")
            else:
                print("Usage: history search <query>")
        else:
            # Show last 50 commands by default
            commands = self.command_history.commands
            start_idx = max(0, len(commands) - 50)
            print("🔹 Command history:")
            for i, cmd in enumerate(commands[start_idx:], start_idx + 1):
                print(f"{i:4} {cmd}")
