import os
import shutil
from pathlib import Path
from datetime import datetime
import psutil

class CommandMethods:
    """Builtin command implementations for a Python terminal."""

    @staticmethod
    def cmd_pwd(current_dir):
        """Print current working directory"""
        print(current_dir)

    @staticmethod
    def cmd_ls(current_dir, args):
        """List directory contents"""
        path = args[0] if args else current_dir
        path = os.path.abspath(path)
        try:
            if not os.path.exists(path):
                print(f"ls: {path}: No such file or directory")
                return
            items = os.listdir(path)
            for item in sorted(items):
                print(item, end='  ')
            if items:
                print()
        except PermissionError:
            print(f"ls: {path}: Permission denied")
        except Exception as e:
            print(f"ls: {e}")

    @staticmethod
    def cmd_cd(current_dir, args):
        """Change directory"""
        path = args[0] if args else os.path.expanduser('~')
        path = os.path.abspath(path if os.path.isabs(path) else os.path.join(current_dir, path))
        if os.path.isdir(path):
            os.chdir(path)
            return path
        else:
            print(f"cd: {path}: No such file or directory")
            return current_dir

    @staticmethod
    def cmd_mkdir(current_dir, args):
        """Create directories"""
        if not args:
            print("mkdir: missing operand")
            return
        for dirname in args:
            path = os.path.abspath(os.path.join(current_dir, dirname))
            try:
                os.makedirs(path, exist_ok=False)
                print(f"✅ Created directory: {path}")
            except FileExistsError:
                print(f"mkdir: {path} already exists")
            except Exception as e:
                print(f"mkdir: {e}")

    @staticmethod
    def cmd_rmdir(current_dir, args):
        """Remove empty directories"""
        if not args:
            print("rmdir: missing operand")
            return
        for dirname in args:
            path = os.path.abspath(os.path.join(current_dir, dirname))
            try:
                os.rmdir(path)
                print(f"✅ Removed directory: {path}")
            except OSError as e:
                print(f"rmdir: {path}: {e}")

    @staticmethod
    def cmd_rm(current_dir, args):
        """Remove files or directories"""
        if not args:
            print("rm: missing operand")
            return
        for filename in args:
            path = os.path.abspath(os.path.join(current_dir, filename))
            try:
                if os.path.isfile(path):
                    os.remove(path)
                    print(f"✅ Removed file: {path}")
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"✅ Removed directory: {path}")
                else:
                    print(f"rm: {path}: No such file or directory")
            except Exception as e:
                print(f"rm: {e}")

    @staticmethod
    def cmd_touch(current_dir, args):
        """Create empty files or update timestamps"""
        if not args:
            print("touch: missing operand")
            return
        for filename in args:
            path = os.path.abspath(os.path.join(current_dir, filename))
            try:
                Path(path).touch(exist_ok=True)
                print(f"✅ Created/updated file: {path}")
            except Exception as e:
                print(f"touch: {e}")

    @staticmethod
    def cmd_cat(current_dir, args):
        """Display file contents"""
        if not args:
            print("cat: missing file operand")
            return
        for filename in args:
            path = os.path.abspath(os.path.join(current_dir, filename))
            try:
                with open(path, 'r') as f:
                    print(f.read(), end='')
            except FileNotFoundError:
                print(f"cat: {path}: No such file or directory")
            except Exception as e:
                print(f"cat: {e}")

    @staticmethod
    def cmd_echo(args):
        """Print text"""
        print(' '.join(args))

    @staticmethod
    def cmd_cp(current_dir, args):
        """Copy file or directory"""
        if len(args) < 2:
            print("cp: missing operand")
            return
        src = os.path.abspath(os.path.join(current_dir, args[0]))
        dest = os.path.abspath(os.path.join(current_dir, args[1]))
        try:
            if os.path.isfile(src):
                shutil.copy2(src, dest)
                print(f"✅ Copied {src} → {dest}")
            elif os.path.isdir(src):
                shutil.copytree(src, dest)
                print(f"✅ Copied directory {src} → {dest}")
            else:
                print(f"cp: {src}: No such file or directory")
        except Exception as e:
            print(f"cp: {e}")

    @staticmethod
    def cmd_mv(current_dir, args):
        """Move/rename file or directory"""
        if len(args) < 2:
            print("mv: missing operand")
            return
        src = os.path.abspath(os.path.join(current_dir, args[0]))
        dest = os.path.abspath(os.path.join(current_dir, args[1]))
        try:
            shutil.move(src, dest)
            print(f"✅ Moved {src} → {dest}")
        except Exception as e:
            print(f"mv: {e}")

    @staticmethod
    def cmd_ps(args):
        """Show running processes"""
        try:
            print(f"{'PID':<8} {'NAME':<25} {'CPU%':<8} {'MEM%':<8} {'STATUS'}")
            print("-"*60)
            for proc in psutil.process_iter(['pid','name','cpu_percent','memory_percent','status']):
                info = proc.info
                print(f"{info['pid']:<8} {info['name']:<25} {info['cpu_percent']:<8.1f} {info['memory_percent']:<8.1f} {info['status']}")
        except Exception as e:
            print(f"ps: {e}")

    @staticmethod
    def cmd_top():
        """Show CPU and memory usage"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            print(f"CPU Usage: {cpu}%")
            print(f"Memory Usage: {mem.percent}% ({mem.used // (1024**3)}GB/{mem.total // (1024**3)}GB)")
        except Exception as e:
            print(f"top: {e}")

    @staticmethod
    def cmd_df():
        """Show disk usage"""
        try:
            partitions = psutil.disk_partitions()
            for part in partitions:
                usage = psutil.disk_usage(part.mountpoint)
                print(f"{part.device} {usage.percent}% used ({usage.used // (1024**3)}GB/{usage.total // (1024**3)}GB)")
        except Exception as e:
            print(f"df: {e}")

    @staticmethod
    def cmd_free():
        """Show memory usage"""
        try:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            print(f"Memory: total={mem.total // (1024**2)}MB, used={mem.used // (1024**2)}MB, free={mem.available // (1024**2)}MB")
            print(f"Swap: total={swap.total // (1024**2)}MB, used={swap.used // (1024**2)}MB, free={swap.free // (1024**2)}MB")
        except Exception as e:
            print(f"free: {e}")

    @staticmethod
    def cmd_clear():
        """Clear terminal"""
        os.system('cls' if os.name=='nt' else 'clear')

    @staticmethod
    def cmd_history(history_commands):
        """Show command history"""
        print("🔹 Command History:")
        for i, cmd in enumerate(history_commands[-50:], start=1):
            print(f"{i:4} {cmd}")

    @staticmethod
    def cmd_help():
        """Show help"""
        print("📌 Available commands:")
        print("File: ls, cd, pwd, mkdir, rmdir, rm, touch, cat, cp, mv, echo")
        print("System: ps, top, df, free")
        print("Utilities: history, clear, help")
        print("Exit: exit, quit")
