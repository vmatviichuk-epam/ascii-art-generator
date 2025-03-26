#!/usr/bin/env python3
"""
ASCII Art Module
This module provides ASCII art patterns and functionality for the ASCII Converter application.
"""

class ASCIIArt:
    def __init__(self):
        # Define patterns using the '1' character - will be replaced with the selected pattern character
        self.art_patterns = {
            'A': ["  1  ", " 1 1 ", "11111", "1   1"],
            'B': ["1111 ", "1   1", "1111 ", "1   1", "1111 "],
            'C': [" 111 ", "1    ", "1    ", " 111 "],
            'D': ["1111 ", "1   1", "1   1", "1111 "],
            'E': ["11111", "1    ", "111  ", "1    ", "11111"],
            'F': ["11111", "1    ", "111  ", "1    ", "1    "],
            'G': [" 111 ", "1    ", "1  11", " 111 "],
            'H': ["1   1", "1   1", "11111", "1   1", "1   1"],
            'I': ["11111", "  1  ", "  1  ", "  1  ", "11111"],
            'J': ["11111", "   1 ", "   1 ", "1  1 ", " 11  "],
            'K': ["1  1 ", "1 1  ", "11   ", "1 1  ", "1  1 "],
            'L': ["1    ", "1    ", "1    ", "1    ", "11111"],
            'M': ["1   1", "11 11", "1 1 1", "1   1", "1   1"],
            'N': ["1   1", "11  1", "1 1 1", "1  11", "1   1"],
            'O': [" 111 ", "1   1", "1   1", "1   1", " 111 "],
            'P': ["1111 ", "1   1", "1111 ", "1    ", "1    "],
            'Q': [" 111 ", "1   1", "1   1", "1  11", " 1111"],
            'R': ["1111 ", "1   1", "1111 ", "1  1 ", "1   1"],
            'S': [" 111 ", "1    ", " 111 ", "    1", " 111 "],
            'T': ["11111", "  1  ", "  1  ", "  1  ", "  1  "],
            'U': ["1   1", "1   1", "1   1", "1   1", " 111 "],
            'V': ["1   1", "1   1", "1   1", " 1 1 ", "  1  "],
            'W': ["1   1", "1   1", "1 1 1", "1 1 1", " 1 1 "],
            'X': ["1   1", " 1 1 ", "  1  ", " 1 1 ", "1   1"],
            'Y': ["1   1", " 1 1 ", "  1  ", "  1  ", "  1  "],
            'Z': ["11111", "   1 ", "  1  ", " 1   ", "11111"],
            '0': [" 111 ", "1   1", "1   1", "1   1", " 111 "],
            '1': ["  1  ", " 11  ", "  1  ", "  1  ", "11111"],
            '2': [" 111 ", "1   1", "   1 ", "  1  ", "11111"],
            '3': ["1111 ", "    1", "  11 ", "    1", "1111 "],
            '4': ["   1 ", "  11 ", " 1 1 ", "11111", "   1 "],
            '5': ["11111", "1    ", "1111 ", "    1", "1111 "],
            '6': [" 111 ", "1    ", "1111 ", "1   1", " 111 "],
            '7': ["11111", "    1", "   1 ", "  1  ", " 1   "],
            '8': [" 111 ", "1   1", " 111 ", "1   1", " 111 "],
            '9': [" 111 ", "1   1", " 1111", "    1", " 111 "],
            ' ': ["     ", "     ", "     ", "     ", "     "],
            '.': ["     ", "     ", "     ", "     ", "  1  "],
            ',': ["     ", "     ", "     ", "  1  ", " 1   "],
            '!': ["  1  ", "  1  ", "  1  ", "     ", "  1  "],
            '?': [" 111 ", "1   1", "  11 ", "     ", "  1  "],
            # Add more characters as needed
        }
        
    def get_pattern(self, pattern_char, char):
        """
        Generate ASCII art pattern for a character using the specified pattern character.
        
        Args:
            pattern_char (str): Character to use for the pattern (e.g., '*', '1', 'o', etc.)
            char (str): The character to convert to ASCII art
            
        Returns:
            list: Lines of ASCII art for the character
        """
        ascii_val = ord(char)
        char = char.upper()  # Use uppercase for consistency
        
        # Get the pattern for the given character or use a default pattern
        if char in self.art_patterns:
            pattern = self.art_patterns[char]
        else:
            # Default pattern for characters not in the dictionary
            pattern = [
                "     ",
                f"  {char}  ",
                f" ({ascii_val}) ",
                "     ",
                "     "
            ]
        
        # Replace the '1' character with the selected pattern character
        return [line.replace('1', pattern_char) for line in pattern]
        
    def generate_art(self, text, pattern_char='1', max_length=15):
        """
        Generate ASCII art for a text string.
        
        Args:
            text (str): Text to convert to ASCII art
            pattern_char (str, optional): Character to use for patterns. Defaults to '1'.
            max_length (int, optional): Maximum text length to process. Defaults to 15.
            
        Returns:
            tuple: (list of art lines, truncated status)
        """
        truncated = False
        
        # Limit text length for better display
        if len(text) > max_length:
            text = text[:max_length]
            truncated = True
            
        # Generate ASCII art for each character
        art_lines = [[] for _ in range(5)]  # 5 lines per character
        
        for char in text:
            art = self.get_pattern(pattern_char, char)
            for i in range(min(len(art), 5)):
                art_lines[i].append(art[i])
        
        # Join the lines together
        result = [" ".join(line) for line in art_lines]
        
        return result, truncated