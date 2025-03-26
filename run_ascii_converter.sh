#!/bin/bash

# Fix for tkinter on macOS
# This script uses the Python version with tkinter support that we installed via Homebrew

# Get the absolute path of the directory this script is in
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use the Homebrew-installed Python 3.9 with tkinter support
PYTHON_CMD="/usr/local/Cellar/python-tk@3.9/3.9.21/bin/python3.9"

# Check if Python exists at the expected location
if [ ! -f "$PYTHON_CMD" ]; then
    echo "Error: Could not find Python at $PYTHON_CMD"
    echo "Falling back to search for other Python installations..."
    
    # Try to find any Python with tkinter support
    for python_path in \
        "/usr/local/bin/python3.9" \
        "/usr/local/opt/python-tk@3.9/bin/python3.9" \
        "python3.9" \
        "python3" \
        "python"
    do
        if command -v $python_path &>/dev/null; then
            PYTHON_CMD=$(command -v $python_path)
            
            # Check if this Python has tkinter
            $PYTHON_CMD -c "import tkinter" &>/dev/null
            if [ $? -eq 0 ]; then
                echo "Found Python with tkinter at: $PYTHON_CMD"
                break
            else
                echo "Found Python at $PYTHON_CMD, but it doesn't have tkinter support."
            fi
        fi
    done
fi

# Final check for Python with tkinter
$PYTHON_CMD -c "import tkinter" &>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: Could not find a Python installation with tkinter support."
    echo "Please ensure that Python with tkinter is installed correctly."
    exit 1
fi

# Install required packages if they're missing
echo "Checking for required packages..."

# Check for pyperclip
$PYTHON_CMD -c "import pyperclip" &>/dev/null
if [ $? -ne 0 ];then
    echo "Installing pyperclip for copy functionality..."
    $PYTHON_CMD -m pip install pyperclip --user || $PYTHON_CMD -m pip install pyperclip
fi

# Check for PIL/Pillow
$PYTHON_CMD -c "from PIL import Image" &>/dev/null
if [ $? -ne 0 ];then
    echo "Installing Pillow for image export functionality..."
    $PYTHON_CMD -m pip install Pillow --user || $PYTHON_CMD -m pip install Pillow
fi

# Run the ASCII converter
echo "Starting ASCII Converter..."

$PYTHON_CMD "$SCRIPT_DIR/ascii_converter.py"