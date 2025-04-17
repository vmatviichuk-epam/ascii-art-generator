# Changes Log
[2024-03-20] Enhanced GUI with improved typography, spacing, and refined black/white/red color scheme.
[2024-03-20] Optimized GUI layout: reduced padding, compact fonts and window size (600x500).
[2024-03-20] Added multi-format export support (PNG, JPG, PDF) with format selector and file dialog.
[2025-03-18] GUI improvements - adjusted spacing, added Copy button, removed image watermark, updated styles to use only red/white colors.
[2025-03-24] Added font size slider (8-20pt) to control ASCII art display size
[2025-03-25] Refactored color scheme to use only black/white/red per design guidelines
[2025-03-25] Enhanced image export to use red color for special characters
[2025-03-25] Removed Docker support and related files to simplify deployment
[2025-03-25] Created constants.py for centralized color management
[2025-03-25] Updated all UI components to use shared color constants
[2025-03-25] Implemented missing core functions in ascii_converter.py (update_art, export_image, clear_input, update_font_size)
[2025-03-25] Added error handling for image export and font loading
[2025-03-25] Added input validation for ASCII art export
[2025-04-15] Updated run script to support Python 3.13 with tkinter and improved virtual environment handling