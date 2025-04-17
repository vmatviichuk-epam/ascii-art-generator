#!/bin/bash

# ASCII Converter Launcher Script
# This script runs the ASCII Converter application with proper tkinter support

# Get the absolute path of the directory this script is in
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Find Python with tkinter support
echo "Finding Python with tkinter support..."

# Try several Python installations
for python_path in \
    "/usr/local/bin/python3.9" \
    "/usr/local/opt/python-tk@3.9/bin/python3.9" \
    "/usr/local/bin/python3" \
    "python3.9" \
    "python3" \
    "python"
do
    if command -v $python_path &>/dev/null; then
        PYTHON_CMD=$(command -v $python_path)
        
        # Check if this Python has tkinter
        if $PYTHON_CMD -c "import tkinter" &>/dev/null; then
            echo "Found Python with tkinter at: $PYTHON_CMD"
            break
        else
            echo "Found Python at $PYTHON_CMD, but it doesn't have tkinter support."
        fi
    fi
done

# Final check for Python with tkinter
if ! $PYTHON_CMD -c "import tkinter" &>/dev/null; then
    echo "Error: Could not find a Python installation with tkinter support."
    echo "Please install Python with tkinter support. For macOS users:"
    echo "  brew install python-tk@3.9"
    exit 1
fi

# Remove any existing virtual environment
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

# Create a fresh virtual environment with the Python that has tkinter
echo "Creating virtual environment with $PYTHON_CMD..."
$PYTHON_CMD -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify tkinter still works in the virtual environment
if ! python -c "import tkinter" &>/dev/null; then
    echo "Error: Virtual environment Python doesn't have tkinter support."
    echo "This may be due to a mismatch between system Python and venv."
    echo "Trying direct execution without virtual environment..."
    $PYTHON_CMD "$SCRIPT_DIR/ascii_converter.py"
    exit 0
fi

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt

# Run the ASCII converter
echo "Starting ASCII Converter..."
python "$SCRIPT_DIR/ascii_converter.py"