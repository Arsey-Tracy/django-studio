"""Code folding utilities for Python"""
import re
from typing import List, Tuple


class CodeFolder:
    """Detects and manages foldable code regions"""
    
    @staticmethod
    def find_foldable_regions(code: str) -> List[Tuple[int, int, str]]:
        """
        Find foldable regions in code.
        Returns list of (start_line, end_line, type)
        """
        lines = code.split('\n')
        regions = []
        stack = []  # Stack of (line_num, indent_level, type)
        
        for line_num, line in enumerate(lines):
            if not line.strip() or line.strip().startswith('#'):
                continue
            
            indent = len(line) - len(line.lstrip())
            content = line.strip()
            
            # Check for foldable keywords
            is_foldable = False
            fold_type = None
            
            if re.match(r'(def|class|if|for|while|with|try)\b', content):
                is_foldable = True
                match = re.match(r'(\w+)', content)
                fold_type = match.group(1) if match else 'block'
            
            # Pop regions that should end
            while stack and stack[-1][1] >= indent and is_foldable:
                start_line, start_indent, region_type = stack.pop()
                if line_num - start_line > 1:  # Only fold if more than 1 line
                    regions.append((start_line, line_num - 1, region_type))
            
            # Push current region
            if is_foldable:
                stack.append((line_num, indent, fold_type))
        
        # Pop remaining regions
        while stack:
            start_line, start_indent, region_type = stack.pop()
            if len(lines) - 1 - start_line > 0:
                regions.append((start_line, len(lines) - 1, region_type))
        
        return regions
    
    @staticmethod
    def get_fold_text(lines: List[str], start: int, end: int) -> str:
        """Get preview text for folded region"""
        if start < len(lines):
            text = lines[start].strip()
            # Truncate if too long
            if len(text) > 40:
                text = text[:37] + '...'
            return text
        return '...'
