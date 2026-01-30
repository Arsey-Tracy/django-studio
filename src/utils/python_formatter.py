"""Python code formatter utility"""
import re


class PythonFormatter:
    """Simple Python code formatter"""
    
    @staticmethod
    def format_code(code: str) -> str:
        """Format Python code with basic rules"""
        lines = code.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Skip empty lines
            if not line.strip():
                formatted_lines.append('')
                continue
            
            # Get indentation
            indent = len(line) - len(line.lstrip())
            content = line.strip()
            
            # Fix spacing around operators
            content = PythonFormatter._fix_operator_spacing(content)
            
            # Fix spacing in function/class definitions
            content = PythonFormatter._fix_definition_spacing(content)
            
            # Add back indentation
            formatted_line = ' ' * indent + content
            formatted_lines.append(formatted_line)
        
        # Join lines and remove trailing whitespace
        result = '\n'.join(formatted_lines)
        
        # Ensure file ends with newline
        if result and not result.endswith('\n'):
            result += '\n'
        
        return result
    
    @staticmethod
    def _fix_operator_spacing(content: str) -> str:
        """Fix spacing around operators"""
        # Add space around assignment operators
        content = re.sub(r'(\w)\s*=\s*(?!=)', r'\1 = ', content)
        
        # Add space around comparison operators
        content = re.sub(r'(\w)\s*(==|!=|<=|>=|<|>)\s*', r'\1 \2 ', content)
        
        # Add space after commas
        content = re.sub(r',(\S)', r', \1', content)
        
        return content
    
    @staticmethod
    def _fix_definition_spacing(content: str) -> str:
        """Fix spacing in function/class definitions"""
        # Fix 'def foo():' -> 'def foo():'
        content = re.sub(r'(def|class)\s+(\w+)\s*\(', r'\1 \2(', content)
        
        # Ensure space after def/class
        content = re.sub(r'(def|class)(\w)', r'\1 \2', content)
        
        return content
