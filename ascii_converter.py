#!/usr/bin/env python3
"""
ASCII Art Application
A GUI application for creating and exporting ASCII art.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from pathlib import Path
from ascii_art import ASCIIArt
from image_export import save_ascii_art_image

class ASCIIArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ASCII Art Creator")
        self.ascii_generator = ASCIIArt()
        
        # Configure root window with compact dimensions
        self.root.geometry("600x500")
        self.root.minsize(500, 400)
        self.root.configure(bg='#FFFFFF')
        
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        style = ttk.Style()
        style.configure(".", background='#FFFFFF')
        
        # Compact styling for frames and widgets
        style.configure("Card.TLabelframe", 
                    padding=6,
                    relief="solid",
                    borderwidth=1,
                    background='#FFFFFF')
        style.configure("Card.TLabelframe.Label", 
                    font=('Helvetica', 11, 'bold'),
                    foreground='#CC0000',
                    background='#FFFFFF')
        style.configure("Main.TLabel",
                    font=('Helvetica', 10),
                    background='#FFFFFF')
        style.configure("Main.TEntry",
                    padding=3)
        style.configure("Action.TButton",
                    padding=(10, 5),
                    font=('Helvetica', 10))
        style.configure("Danger.TButton",
                    padding=(10, 5),
                    font=('Helvetica', 10))
        style.configure("Main.TFrame",
                    background='#FFFFFF')
        
    def setup_ui(self):
        # Main container with reduced padding
        main_container = ttk.Frame(self.root, padding="10", style="Main.TFrame")
        main_container.grid(row=0, column=0, sticky="nsew")
        
        # Title Label
        title_label = ttk.Label(main_container,
                            text="ASCII Art Creator",
                            font=('Helvetica', 14, 'bold'),
                            foreground='#CC0000',
                            style="Main.TLabel")
        title_label.grid(row=0, column=0, pady=(0, 10), sticky="nw")
        
        # Input frame with compact spacing
        input_frame = ttk.LabelFrame(main_container,
                                 text="Create Your Art",
                                 style="Card.TLabelframe")
        input_frame.grid(row=1, column=0, padx=2, pady=(0, 8), sticky="new")
        
        # Text input with reduced padding
        ttk.Label(input_frame,
               text="Enter Text:",
               style="Main.TLabel").grid(row=0, column=0, padx=4, pady=4, sticky="w")
        self.text_input = ttk.Entry(input_frame, width=45, style="Main.TEntry")
        self.text_input.grid(row=0, column=1, padx=4, pady=4, sticky="ew")
        self.text_input.bind('<KeyRelease>', self.update_art)
        
        # Pattern input with compact layout
        ttk.Label(input_frame,
               text="Pattern:",
               style="Main.TLabel").grid(row=1, column=0, padx=4, pady=4, sticky="w")
        pattern_container = ttk.Frame(input_frame, style="Main.TFrame")
        pattern_container.grid(row=1, column=1, sticky="w", padx=4, pady=4)
        
        self.pattern_input = ttk.Entry(pattern_container, width=3, style="Main.TEntry")
        self.pattern_input.pack(side=tk.LEFT)
        self.pattern_input.insert(0, "*")
        self.pattern_input.bind('<KeyRelease>', self.update_art)
        
        ttk.Label(pattern_container,
               text="(single character)",
               style="Main.TLabel",
               font=('Helvetica', 9, 'italic')).pack(side=tk.LEFT, padx=4)
        
        # Font size slider
        font_size_frame = ttk.Frame(input_frame, style="Main.TFrame")
        font_size_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=4, pady=4)
        
        ttk.Label(font_size_frame,
               text="Font Size:",
               style="Main.TLabel").pack(side=tk.LEFT, padx=(0,4))
        
        self.font_size_var = tk.IntVar(value=10)
        self.font_size_slider = ttk.Scale(font_size_frame,
                                      from_=8,
                                      to=20,
                                      orient=tk.HORIZONTAL,
                                      variable=self.font_size_var,
                                      command=self.update_font_size)
        self.font_size_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
        
        ttk.Label(font_size_frame,
               textvariable=self.font_size_var,
               style="Main.TLabel").pack(side=tk.LEFT, padx=4)

        # ASCII Art display with optimized size
        display_frame = ttk.LabelFrame(main_container,
                                   text="Preview",
                                   style="Card.TLabelframe")
        display_frame.grid(row=2, column=0, padx=2, pady=8, sticky="nsew")
        
        text_container = ttk.Frame(display_frame, style="Main.TFrame")
        text_container.grid(row=0, column=0, padx=3, pady=3, sticky="nsew")
        
        y_scrollbar = ttk.Scrollbar(text_container)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        x_scrollbar = ttk.Scrollbar(text_container, orient=tk.HORIZONTAL)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.art_display = tk.Text(text_container,
                               height=12,
                               width=55,
                               font=('Courier', self.font_size_var.get()),
                               wrap=tk.NONE,
                               xscrollcommand=x_scrollbar.set,
                               yscrollcommand=y_scrollbar.set,
                               relief="solid",
                               borderwidth=1,
                               bg='#FFFFFF',
                               fg='#000000')
        self.art_display.pack(expand=True, fill=tk.BOTH, padx=2, pady=2)
        
        y_scrollbar.config(command=self.art_display.yview)
        x_scrollbar.config(command=self.art_display.xview)
        
        # Export options frame
        export_frame = ttk.Frame(main_container, style="Main.TFrame")
        export_frame.grid(row=3, column=0, padx=2, pady=(5,5))
        
        ttk.Label(export_frame,
                text="Format:",
                style="Main.TLabel").pack(side=tk.LEFT, padx=(0,4))
                
        self.format_var = tk.StringVar(value="png")
        for fmt in ["PNG", "JPG", "PDF"]:
            ttk.Radiobutton(export_frame,
                        text=fmt,
                        value=fmt.lower(),
                        variable=self.format_var,
                        style="Main.TLabel").pack(side=tk.LEFT, padx=4)
        
        # Buttons with compact layout
        button_frame = ttk.Frame(main_container, style="Main.TFrame")
        button_frame.grid(row=4, column=0, padx=2, pady=(5,5))
        
        ttk.Button(button_frame,
                text="Export as Image",
                style="Action.TButton",
                command=self.export_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame,
                text="Clear",
                style="Danger.TButton",
                command=self.clear_input).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
            
    def update_art(self, event=None):
        text = self.text_input.get()
        pattern_char = self.pattern_input.get()[:1] or "*"  # Use first character or default to *
        
        if text:
            art_lines, truncated = self.ascii_generator.generate_art(text, pattern_char)
            self.art_display.delete(1.0, tk.END)
            self.art_display.insert(tk.END, "\n".join(art_lines))
            
            if truncated:
                self.art_display.insert(tk.END, "\n\nNote: Text was truncated to fit display")
        else:
            self.art_display.delete(1.0, tk.END)
            
    def export_image(self):
        text = self.text_input.get()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text first!")
            return
            
        pattern_char = self.pattern_input.get()[:1] or "*"
        art_lines = self.art_display.get(1.0, tk.END).splitlines()
        
        # Get selected format
        format_ext = self.format_var.get()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"ascii_art_{timestamp}.{format_ext}"
        
        # Configure file types with all supported formats
        file_types = [
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg;*.jpeg"),
            ("PDF files", "*.pdf"),
            ("All files", "*.*")
        ]
        
        # Set initial directory to Downloads
        initial_dir = str(Path.home() / "Downloads")
            
        filename = filedialog.asksaveasfilename(
            defaultextension=f".{format_ext}",
            filetypes=file_types,
            initialfile=default_filename,
            initialdir=initial_dir,
            title="Save ASCII Art"
        )
        
        if filename:
            try:
                file_path = save_ascii_art_image(art_lines, pattern_char, filename)
                messagebox.showinfo("Success", f"ASCII art saved as:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
            
    def clear_input(self):
        self.text_input.delete(0, tk.END)
        self.pattern_input.delete(0, tk.END)
        self.pattern_input.insert(0, "*")
        self.art_display.delete(1.0, tk.END)

    def update_font_size(self, event=None):
        # Update the font size of the ASCII art display
        current_size = self.font_size_var.get()
        self.art_display.configure(font=('Courier', current_size))
        self.update_art()  # Refresh the display

if __name__ == "__main__":
    root = tk.Tk()
    app = ASCIIArtApp(root)
    root.mainloop()