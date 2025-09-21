import readline
import glob
from typing import Optional, List

class EnhancedAutoCompleter:
    """Command and file tab completion"""
    
    def __init__(self, terminal_instance):
        self.terminal = terminal_instance
        self.commands = ['ls', 'cd', 'pwd', 'mkdir', 'rmdir', 'rm', 'cp', 'mv', 'touch', 'cat', 'echo', 'ps', 'top', 'df', 'free', 'history', 'clear', 'help', 'exit']
    
    def complete(self, text: str, state: int) -> Optional[str]:
        line = readline.get_line_buffer()
        completions = self.get_completions(text, line)
        if state < len(completions):
            return completions[state]
        return None
    
    def get_completions(self, text: str, line: str) -> List[str]:
        completions = []

        # Suggest commands
        if line.strip() == text or line.split()[0] == text:
            completions.extend([cmd for cmd in self.commands if cmd.startswith(text)])
            # Add previous commands from history
            history_suggestions = self.terminal.command_history.get_suggestions(text)
            completions.extend(history_suggestions)

        # Suggest files/folders
        try:
            matches = glob.glob(f"{text}*")
            completions.extend([m.replace(' ', '\\ ') if ' ' in m else m for m in matches])
        except Exception:
            pass

        return sorted(list(set(completions)))

