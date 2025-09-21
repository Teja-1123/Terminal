from ai.ai_interpreter import AICommandInterpreter
from history.command_history import EnhancedCommandHistory
from completion.auto_completer import EnhancedAutoCompleter
from commands.core_commands import CommandMethods
import readline
import os

class PythonTerminal:
    def __init__(self):
        self.clear_screen()

        self.current_dir = os.getcwd()
        self.ai_interpreter = AICommandInterpreter()
        self.command_history = EnhancedCommandHistory()
        self.auto_completer = EnhancedAutoCompleter(self)
        self.setup_readline()
    
    # def setup_readline(self):
    #     readline.set_completer(self.auto_completer.complete)
    #     readline.parse_and_bind("tab: complete")
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear') 
    def setup_readline(self):
        try:
            readline.set_completer(self.auto_completer.complete)
            readline.parse_and_bind("tab: complete")
            readline.set_completer_delims(' \t\n=')
            # Load last 100 commands into readline
            for cmd in self.command_history.commands[-100:]:
                readline.add_history(cmd)
        except ImportError:
            print("⚠️ Readline not available - auto-completion disabled")

    
    def execute_command(self, command):
        if not command.strip():
            return

        # Add to history
        self.command_history.add_command(command)

        parts = command.strip().split()
        cmd = parts[0].lower() if parts else ""

        # Check built-in first
        if cmd in ['exit', 'quit', 'pwd', 'ls', 'cd', 'mkdir', 'rmdir', 'rm', 'touch', 'cat', 'cp', 'mv', 'echo', 'ps', 'top', 'df', 'free', 'history', 'clear', 'help']:
            self._execute_single_command(command)
            return

        # Otherwise, treat as natural language
        if self.ai_interpreter.is_natural_language_query(command):
            print(f"🤖 Interpreting: {command}")
            cmds = self.ai_interpreter.interpret_natural_language(command)
            if cmds:
                for c in cmds:
                    self._execute_single_command(c)
            else:
                print(f"❌ Sorry, I couldn't understand: '{command}'")
                print("💡 Try: 'create a folder called test' or 'ls'")


    
    def _execute_single_command(self, command):
        parts = command.strip().split()
        if not parts:
            return
        cmd, args = parts[0], parts[1:]

        # Built-in commands
        if cmd == 'pwd':
            CommandMethods.cmd_pwd(self.current_dir)
        elif cmd == 'ls':
            CommandMethods.cmd_ls(self.current_dir, args)
        elif cmd == 'cd':
            CommandMethods.cmd_cd(self.current_dir, args)  # fixed: was cmd_touch, should be cmd_cd
        elif cmd == 'mkdir':
            CommandMethods.cmd_mkdir(self.current_dir, args)
        elif cmd == 'rm':
            CommandMethods.cmd_rm(self.current_dir, args)
        elif cmd == 'cat':
            CommandMethods.cmd_cat(self.current_dir, args)
        elif cmd == 'cp':
            CommandMethods.cmd_cp(self.current_dir, args)
        elif cmd == 'mv':
            CommandMethods.cmd_mv(self.current_dir, args)
        elif cmd == 'echo':
            CommandMethods.cmd_echo(args)
        elif cmd == 'ps':
            CommandMethods.cmd_ps(args)
        elif cmd == 'top':
            CommandMethods.cmd_top()
        elif cmd == 'df':
            CommandMethods.cmd_df()
        elif cmd == 'free':
            CommandMethods.cmd_free()
        elif cmd == 'history':
            CommandMethods.cmd_history(args)
        elif cmd == 'clear':
            CommandMethods.cmd_clear()
        elif cmd == 'help':
            CommandMethods.cmd_help()
        elif cmd in ['exit', 'quit']:
            print("👋 Goodbye!")
            exit(0)

        else:
            # Unknown command: suggestions
            print(f"❌ Unknown command: {cmd}")
            
            # Suggest built-in commands starting with same letters
            suggestions = [c for c in self.auto_completer.commands if c.startswith(cmd)]
            if suggestions:
                print("💡 Did you mean:")
                for s in suggestions[:5]:  # show max 5 suggestions
                    print(f"   • {s}")

            # Suggest recent history commands
            history_suggestions = [h for h in reversed(self.command_history.commands) if h.startswith(cmd)]
            if history_suggestions:
                print("🕘 Recently used similar commands:")
                for s in history_suggestions[:5]:
                    print(f"   • {s}")

            print("📌 Type 'help' to see all available commands")

    
    def get_prompt(self):
        return f"{self.current_dir}$ "
    
    def run(self):
        self.clear_screen()
        print("🚀 Welcome to PythonTerminal v2.0!")
        print("🤖 You can type commands or natural language queries.")
        print("📁 File commands: ls, cd, mkdir, rmdir, touch, rm")
        print("🖥️ System commands: show running processes, display system information")
        print("💡 Tip: Try 'create a folder called test' or 'make a file named example.txt'")
        print("Type 'exit' or press Ctrl+D to quit.")

        while True:
            try:
                command = input(self.get_prompt())
                self.execute_command(command)
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                break
if __name__ == '__main__':
    terminal = PythonTerminal()
    terminal.run()
