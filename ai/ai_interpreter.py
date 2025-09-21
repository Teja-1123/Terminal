# import re
# from typing import List, Optional

# class AICommandInterpreter:
#     """AI-driven natural language command interpreter"""
    
#     def __init__(self):
#         self.command_patterns = {
#             r'(?:create|make)\s+(?:a\s+)?(?:folder|directory)\s+(?:called\s+)?["\']?([^"\']+)["\']?': 'mkdir {}',
#             r'(?:delete|remove)\s+(?:the\s+)?(?:folder|directory)\s+["\']?([^"\']+)["\']?': 'rmdir {}',
#             r'(?:list|show)\s+(?:files|contents)': 'ls',
#         }
#         self.fallback_patterns = {
#             r'.*(?:create|make).*(?:folder|directory).*': "Try: 'create a folder called foldername'",
#         }
    
#     def interpret_natural_language(self, query: str) -> Optional[List[str]]:
#         query = query.lower().strip()
#         for pattern, cmd in self.command_patterns.items():
#             match = re.search(pattern, query)
#             if match:
#                 return [cmd.format(*match.groups())] if '{}' in cmd else [cmd]
#         return None
    
#     def is_natural_language_query(self, input_text: str) -> bool:
#         direct_commands = ['ls', 'cd', 'mkdir', 'rmdir', 'rm', 'cp', 'mv', 'cat']
#         first_word = input_text.strip().split()[0].lower() if input_text.strip() else ''
#         if first_word in direct_commands:
#             return False
#         nl_indicators = ['create', 'make', 'delete', 'remove', 'show', 'list', 'display']
#         return any(indicator in input_text.lower() for indicator in nl_indicators)




import re
from typing import List, Optional

class AICommandInterpreter:
    """AI-driven natural language command interpreter"""
    
    def __init__(self):
        self.command_patterns = {
            # Create a folder: match full name after "create ... called"
            r'(?:create|make)\s+(?:a\s+)?(?:folder|directory)\s+(?:called\s+)?["\']?(.+?)["\']?$': 'mkdir "{}"',
            # Create a file: match full name after "create ... named"
            r'(?:create|make)\s+(?:a\s+)?file\s+(?:named\s+)?["\']?(.+?)["\']?$': 'touch "{}"',
            # Delete folder
            r'(?:delete|remove)\s+(?:the\s+)?(?:folder|directory)\s+["\']?(.+?)["\']?$': 'rmdir "{}"',
            # List files
            r'(?:list|show)\s+(?:files|contents)': 'ls',
        }

    def interpret_natural_language(self, query: str) -> Optional[List[str]]:
        query = query.lower().strip()
        for pattern, cmd in self.command_patterns.items():
            match = re.search(pattern, query)
            if match:
                return [cmd.format(match.group(1).strip())]  # use the full captured name
        return None
    
    def is_natural_language_query(self, input_text: str) -> bool:
        direct_commands = ['ls', 'cd', 'mkdir', 'rmdir', 'rm', 'cp', 'mv', 'cat', 'touch']
        first_word = input_text.strip().split()[0].lower() if input_text.strip() else ''
        if first_word in direct_commands:
            return False
        nl_indicators = ['create', 'make', 'delete', 'remove', 'show', 'list', 'display']
        return any(indicator in input_text.lower() for indicator in nl_indicators)
