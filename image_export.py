#!/usr/bin/env python3
"""
Image Export Module
This module provides functionality to export ASCII art as image files.
"""
import os
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from constants import COLORS


def ascii_to_image(ascii_lines, pattern_char, font_size=12, padding=5):
    """
    Convert ASCII art to an image.
    
    Args:
        ascii_lines (list): Lines of ASCII art
        pattern_char (str): The character used for the ASCII art
        font_size (int): Size of the font (matches UI font size)
        padding (int): Padding around the text (matches UI padding)
        
    Returns:
        PIL.Image: Generated image
    """
    # Filter out empty lines and info messages
    art_lines = [line for line in ascii_lines if line and not line.startswith('\n') and 
                not line.startswith('Text was') and not line.startswith('ASCII art created')]
    
    if not art_lines:
        # If no valid art lines, create a simple message
        art_lines = ["No ASCII art to export"]
    
    # Use Courier font to match UI exactly
    try:
        font = ImageFont.truetype('Courier', font_size)
    except IOError:
        try:
            font = ImageFont.truetype('Courier New', font_size)
        except IOError:
            # Fallback to default as last resort
            font = ImageFont.load_default()
    
    # Calculate image size based on text
    max_width = 0
    total_height = 0
    
    # Use temporary ImageDraw to calculate text dimensions
    temp_img = Image.new('RGB', (1, 1), COLORS['bg'])
    temp_draw = ImageDraw.Draw(temp_img)
    
    for line in art_lines:
        width, height = temp_draw.textbbox((0, 0), line, font=font)[2:]
        max_width = max(max_width, width)
        total_height += height
    
    # Add padding
    img_width = max_width + (padding * 2)
    img_height = total_height + (padding * 2)
    
    # Create the image with white background
    img = Image.new('RGB', (img_width, img_height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    # Draw the ASCII art with special character coloring
    y_position = padding
    for line in art_lines:
        # Use red color for special characters, black for regular text
        text_color = COLORS['accent'] if any(c in '!?.,*#@$%&' for c in line) else COLORS['text']
        draw.text((padding, y_position), line, font=font, fill=text_color)
        _, _, _, line_height = draw.textbbox((padding, y_position), line, font=font)
        y_position = line_height
    
    return img


def save_ascii_art_image(ascii_lines, pattern_char, filename=None, download_folder=None):
    """
    Save ASCII art as an image in the downloads folder.
    Supports JPG, PNG, and PDF formats.
    
    Args:
        ascii_lines (list): Lines of ASCII art
        pattern_char (str): The character used for the ASCII art
        filename (str, optional): Custom filename. Defaults to None.
        download_folder (str, optional): Custom download folder path. Defaults to None.
        
    Returns:
        str: Path to the saved image
    """
    # Create image from ASCII art
    img = ascii_to_image(ascii_lines, pattern_char)
    
    # Determine download folder
    if not download_folder:
        download_folder = str(Path.home() / "Downloads")
    
    # Ensure directory exists
    os.makedirs(download_folder, exist_ok=True)
    
    # Generate filename if not provided
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ascii_art_{timestamp}"
    
    # Handle different file formats based on extension
    if filename.lower().endswith(('.jpg', '.jpeg')):
        file_path = os.path.join(download_folder, filename)
        img.save(file_path, 'JPEG', quality=95)
    elif filename.lower().endswith('.png'):
        file_path = os.path.join(download_folder, filename)
        img.save(file_path, 'PNG')
    elif filename.lower().endswith('.pdf'):
        file_path = os.path.join(download_folder, filename)
        # Convert to RGB mode for PDF
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(file_path, 'PDF', resolution=300.0)
    else:
        # Default to PNG if no extension provided
        file_path = os.path.join(download_folder, f"{filename}.png")
        img.save(file_path, 'PNG')
    
    return file_path