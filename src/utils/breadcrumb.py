"""Code breadcrumb navigation"""
import re
from typing import List, Tuple, Optional


class Breadcrumb:
    """Generates breadcrumb trail showing current code location"""
    
    @staticmethod
    def get_breadcrumb(code: str, cursor_line: int) -> List[Tuple[str, int]]:
        """
        Get breadcrumb trail for cursor position.
        Returns list of (name, line_number) tuples from file to current scope
        """
        breadcrumb = []
        
        lines = code.split('\n')
        if cursor_line >= len(lines):
            cursor_line = len(lines) - 1
        
        # Get indentation of current line
        current_indent = 0
        if cursor_line < len(lines):
            line = lines[cursor_line]
            current_indent = len(line) - len(line.lstrip())
        
        # Walk backwards through lines to find containing scope
        for line_num in range(cursor_line, -1, -1):
            if line_num >= len(lines):
                continue
            
            line = lines[line_num]
            if not line.strip():
                continue
            
            indent = len(line) - len(line.lstrip())
            
            # Only consider lines with less indentation (parent scopes)
            if indent >= current_indent and line_num != cursor_line:
                continue
            
            # Check for class definition
            class_match = re.match(r'\s*class\s+(\w+)', line)
            if class_match and indent < current_indent:
                breadcrumb.insert(0, (class_match.group(1), line_num))
                current_indent = indent
                continue
            
            # Check for function definition
            def_match = re.match(r'\s*def\s+(\w+)', line)
            if def_match and indent < current_indent:
                breadcrumb.insert(0, (def_match.group(1), line_num))
                current_indent = indent
                continue
        
        # Add file name at the beginning
        breadcrumb.insert(0, ('file', 0))
        
        return breadcrumb
    
    @staticmethod
    def format_breadcrumb(breadcrumb: List[Tuple[str, int]]) -> str:
        """Format breadcrumb as readable string"""
        if not breadcrumb:
            return 'file'
        
        parts = []
        for name, line_num in breadcrumb:
            if name == 'file':
                parts.append('📄')
            elif name.startswith('class') or re.match(r'^[A-Z]', name):
                parts.append(f'🔵 {name}')
            else:
                parts.append(f'⚙ {name}')
        
        return ' > '.join(parts)
