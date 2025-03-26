# ASCII Art Creator

A simple GUI application that creates ASCII art and allows exporting it as images.

## Features

- Create ASCII art from text in real-time
- Customize the pattern character used (*, #, @, etc.)
- Export ASCII art in multiple formats:
  - PNG (high-quality lossless)
  - JPEG (compressed)
  - PDF (vector format)
- User-friendly interface
- Monospaced font display

## Requirements

- Python 3.x
- Tkinter (included in standard Python distribution)
- Pillow (for image export)

## Installation

1. Clone or download this repository
2. Install the requirements:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application with:
```
python ascii_converter.py
```

Or on macOS, use the provided shell script:
```
sh run_ascii_converter.sh
```

1. Enter text in the input box
2. Choose a pattern character (default is *)
3. The ASCII art will be generated automatically
4. Select your preferred export format (PNG, JPG, or PDF)
5. Click "Export as Image" to save your artwork
6. Use "Clear" to start over

## License

This project is open source and available under the MIT License.