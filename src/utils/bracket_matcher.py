"""Bracket matching utility for code editor"""
from typing import Optional, Tuple


class BracketMatcher:
    """Detects and matches bracket pairs"""
    
    BRACKET_PAIRS = {
        '(': ')',
        '[': ']',
        '{': '}',
        '"': '"',
        "'": "'",
    }
    
    OPENING_BRACKETS = set(BRACKET_PAIRS.keys())
    CLOSING_BRACKETS = {v: k for k, v in BRACKET_PAIRS.items()}
    
    @staticmethod
    def find_matching_bracket(text: str, pos: int) -> Optional[Tuple[int, int]]:
        """
        Find matching bracket pair.
        Returns (bracket_pos, match_pos) or None if no match found
        """
        if pos >= len(text):
            return None
        
        char = text[pos]
        
        # Check if cursor is on opening bracket
        if char in BracketMatcher.OPENING_BRACKETS:
            match_pos = BracketMatcher._find_closing(text, pos, char)
            if match_pos is not None:
                return (pos, match_pos)
        
        # Check if cursor is on closing bracket
        elif char in BracketMatcher.CLOSING_BRACKETS:
            match_pos = BracketMatcher._find_opening(text, pos, char)
            if match_pos is not None:
                return (match_pos, pos)
        
        return None
    
    @staticmethod
    def _find_closing(text: str, start: int, opening_char: str) -> Optional[int]:
        """Find closing bracket matching the opening bracket at start position"""
        closing_char = BracketMatcher.BRACKET_PAIRS[opening_char]
        count = 1
        
        for i in range(start + 1, len(text)):
            char = text[i]
            
            # Skip strings
            if opening_char not in ('"', "'"):
                if char in ('"', "'"):
                    # Simple string skip - doesn't handle escapes perfectly
                    quote = char
                    i += 1
                    while i < len(text) and text[i] != quote:
                        if text[i] == '\\':
                            i += 1
                        i += 1
                    continue
            
            if char == opening_char:
                count += 1
            elif char == closing_char:
                count -= 1
                if count == 0:
                    return i
        
        return None
    
    @staticmethod
    def _find_opening(text: str, start: int, closing_char: str) -> Optional[int]:
        """Find opening bracket matching the closing bracket at start position"""
        opening_char = BracketMatcher.CLOSING_BRACKETS[closing_char]
        count = 1
        
        for i in range(start - 1, -1, -1):
            char = text[i]
            
            # Skip strings
            if closing_char not in ('"', "'"):
                if char in ('"', "'"):
                    quote = char
                    i -= 1
                    while i >= 0 and text[i] != quote:
                        if text[i] == '\\':
                            i -= 1
                        i -= 1
                    continue
            
            if char == closing_char:
                count += 1
            elif char == opening_char:
                count -= 1
                if count == 0:
                    return i
        
        return None
