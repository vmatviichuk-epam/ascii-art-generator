#!/usr/bin/env python3
"""
Unit tests for the ASCII Art module.
This file contains tests for the ASCIIArt class functionality.
"""

import unittest
from ascii_art import ASCIIArt

class TestASCIIArt(unittest.TestCase):
    """Test cases for the ASCIIArt class."""
    
    def setUp(self):
        """Set up test fixtures before each test method is run."""
        self.ascii_art = ASCIIArt()
    
    def test_init(self):
        """Test initialization of ASCIIArt class."""
        self.assertIsInstance(self.ascii_art, ASCIIArt)
        self.assertIsInstance(self.ascii_art.art_patterns, dict)
        self.assertIn('A', self.ascii_art.art_patterns)
        self.assertIn('Z', self.ascii_art.art_patterns)
        self.assertIn('0', self.ascii_art.art_patterns)
        self.assertIn(' ', self.ascii_art.art_patterns)
    
    def test_get_pattern_known_character(self):
        """Test retrieving patterns for known characters."""
        # Test a letter
        a_pattern = self.ascii_art.get_pattern('*', 'A')
        expected_a = ["  *  ", " * * ", "*****", "*   *"]
        self.assertEqual(a_pattern, expected_a)
        
        # Test a number
        zero_pattern = self.ascii_art.get_pattern('#', '0')
        expected_zero = [" ### ", "#   #", "#   #", "#   #", " ### "]
        self.assertEqual(zero_pattern, expected_zero)
        
        # Test special character
        space_pattern = self.ascii_art.get_pattern('@', ' ')
        expected_space = ["     ", "     ", "     ", "     ", "     "]
        self.assertEqual(space_pattern, expected_space)
    
    def test_get_pattern_unknown_character(self):
        """Test retrieving patterns for unknown characters."""
        # Test a character not in the patterns dictionary
        unknown_pattern = self.ascii_art.get_pattern('*', '$')
        # ASCII value of '$' is 36
        expected_unknown = [
            "     ",
            "  $  ",
            " (36) ",
            "     ",
            "     "
        ]
        self.assertEqual(unknown_pattern, expected_unknown)
    
    def test_get_pattern_lowercase_character(self):
        """Test that lowercase characters are converted to uppercase."""
        a_upper_pattern = self.ascii_art.get_pattern('*', 'A')
        a_lower_pattern = self.ascii_art.get_pattern('*', 'a')
        self.assertEqual(a_upper_pattern, a_lower_pattern)
    
    def test_generate_art_simple(self):
        """Test generating ASCII art for a simple string."""
        text = "ABC"
        result, truncated = self.ascii_art.generate_art(text, '*')
        
        expected = [
            "  *   ****   *** ",
            " * *  *   * *    ",
            "***** ****  *    ",
            "*   * *   * *    ",
            "****   *** "
        ]
        
        self.assertEqual(result, expected)
        self.assertFalse(truncated)
    
    def test_generate_art_mixed_case(self):
        """Test generating ASCII art with mixed case characters."""
        text = "Abc"
        result, truncated = self.ascii_art.generate_art(text, '#')
        
        expected = [
            "  #   ####   ### ",
            " # #  #   # #    ",
            "##### ####  #    ",
            "#   # #   # #    ",
            "####   ### "
        ]
        
        self.assertEqual(result, expected)
        self.assertFalse(truncated)
    
    def test_generate_art_truncation(self):
        """Test that text is truncated if it exceeds max_length."""
        long_text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        max_length = 5
        
        result, truncated = self.ascii_art.generate_art(long_text, '*', max_length)
        
        # Should only have the first 5 characters (ABCDE)
        self.assertEqual(len("".join(result[0]).strip()), 27)  # Approximate check for 5 characters
        self.assertTrue(truncated)
        
        # Verify first 5 characters are present
        for char in "ABCDE":
            art_chunk, _ = self.ascii_art.generate_art(char, '*')
            # At least one line of the character's art should be in the result
            found = False
            for line in art_chunk:
                if line.strip() and any(line.strip() in res_line for res_line in result):
                    found = True
                    break
            self.assertTrue(found, f"Character {char} art not found in result")
    
    def test_generate_art_custom_pattern_char(self):
        """Test using different pattern characters."""
        text = "HI"
        result1, _ = self.ascii_art.generate_art(text, '*')
        result2, _ = self.ascii_art.generate_art(text, '#')
        
        # Results should be different with different pattern characters
        self.assertNotEqual(result1, result2)
        
        # Verify * patterns replaced with #
        for i in range(len(result1)):
            line1 = result1[i]
            line2 = result2[i]
            self.assertEqual(line1.replace('*', '#'), line2)
    
    def test_generate_art_empty_string(self):
        """Test generating ASCII art for an empty string."""
        result, truncated = self.ascii_art.generate_art("", '*')
        
        # Should return 5 empty lines
        expected = ['', '', '', '', '']
        self.assertEqual(result, expected)
        self.assertFalse(truncated)
    
    def test_generate_art_special_characters(self):
        """Test generating ASCII art with special characters."""
        text = "!?."
        result, truncated = self.ascii_art.generate_art(text, '+')
        
        expected = [
            "  +    +++       ",
            "  +   +   +      ",
            "  +     ++       ",
            "                 ",
            "  +     +     +  "
        ]
        
        self.assertEqual(result, expected)
        self.assertFalse(truncated)
    
    def test_generate_art_unknown_characters(self):
        """Test generating ASCII art with characters not in the pattern dictionary."""
        text = "@#$"
        result, truncated = self.ascii_art.generate_art(text, '*')
        
        # Check that the ASCII values are included
        self.assertIn("@", result[1])
        self.assertIn("#", result[1])
        self.assertIn("$", result[1])
        self.assertIn("(64)", result[2])  # ASCII value of @
        self.assertIn("(35)", result[2])  # ASCII value of #
        self.assertIn("(36)", result[2])  # ASCII value of $
        
        self.assertFalse(truncated)

if __name__ == '__main__':
    unittest.main()