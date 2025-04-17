# ASCII Art Creator

A simple GUI application that creates ASCII art and allows exporting it as images.

## Features

- Create ASCII art from text in real-time
- Customize the pattern character used (*, #, @, etc.)
- Export ASCII art in multiple formats:
  - PNG (high-quality lossless)
  - JPEG (compressed)
  - PDF (vector format)
- User-friendly interface with consistent black/white/red color scheme
- Monospaced font display with adjustable size (8-20pt)

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

Run the application using sh:
```
sh run_ascii_converter.sh
```

## Application Usage

1. Enter text in the input box
2. Choose a pattern character (default is *)
3. Adjust font size using the slider if needed (8-20pt)
4. The ASCII art will be generated automatically
5. Select your preferred export format (PNG, JPG, or PDF)
6. Click "Export as Image" to save your artwork
7. Use "Clear" to start over

## Design Guidelines

- Strict color scheme: black (#000000), white (#FFFFFF), and red (#FF0000)
- Special characters in exported images are highlighted in red
- Consistent monospaced font (Courier) for ASCII art display
- Clean, minimal interface with optimized spacing

## License

This project is open source and available under the MIT License.