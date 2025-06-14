# Metadata-Extractor Versi Deployement Ke Github

import os
import csv
import datetime
import threading
import json
import hashlib
from typing import Dict, List, Any
from pathlib import Path

# GUI imports
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
except ImportError:
    raise ImportError("Please install tkinterdnd2: pip install tkinterdnd2")

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog

# Metadata extraction imports
try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: PIL/Pillow not available. Image metadata extraction disabled.")

try:
    from pymediainfo import MediaInfo
    MEDIAINFO_AVAILABLE = True
except ImportError:
    MEDIAINFO_AVAILABLE = False
    print("Warning: pymediainfo not available. Media metadata extraction disabled.")

# Supported file extensions
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.tiff', '.tif', '.png', '.bmp', '.gif', '.webp'}
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.m4v', '.webm'}
AUDIO_EXTENSIONS = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'}
DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt', '.rtf'}

class MetadataExtractor:
    """Enhanced metadata extraction with error handling and performance optimization"""
    
    @staticmethod
    def calculate_file_hash(filepath: str, algorithm: str = 'md5') -> str:
        """Calculate file hash for integrity verification"""
        try:
            hash_obj = hashlib.new(algorithm)
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except Exception as e:
            return f"Error: {str(e)}"
    
    @staticmethod
    def get_file_type_category(filepath: str) -> str:
        """Determine file category based on extension"""
        ext = Path(filepath).suffix.lower()
        if ext in IMAGE_EXTENSIONS:
            return 'image'
        elif ext in VIDEO_EXTENSIONS:
            return 'video'
        elif ext in AUDIO_EXTENSIONS:
            return 'audio'
        elif ext in DOCUMENT_EXTENSIONS:
            return 'document'
        else:
            return 'other'
    
    @staticmethod
    def extract_basic_metadata(filepath: str) -> Dict[str, Any]:
        """Extract basic file system metadata"""
        try:
            stat = os.stat(filepath)
            path_obj = Path(filepath)
            
            return {
                'filename': path_obj.name,
                'filepath': str(path_obj.absolute()),
                'directory': str(path_obj.parent),
                'extension': path_obj.suffix.lower(),
                'file_type': MetadataExtractor.get_file_type_category(filepath),
                'size_bytes': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'created': datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'accessed': datetime.datetime.fromtimestamp(stat.st_atime).isoformat(),
                'permissions': oct(stat.st_mode)[-3:],
                'md5_hash': MetadataExtractor.calculate_file_hash(filepath, 'md5'),
                'extraction_timestamp': datetime.datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': f"Failed to extract basic metadata: {str(e)}"}
    
    @staticmethod
    def extract_image_metadata(filepath: str) -> Dict[str, Any]:
        """Extract EXIF data from images"""
        if not PIL_AVAILABLE:
            return {'error': 'PIL/Pillow not available'}
        
        metadata = {}
        try:
            with Image.open(filepath) as img:
                # Basic image info
                metadata.update({
                    'image_width': img.width,
                    'image_height': img.height,
                    'image_mode': img.mode,
                    'image_format': img.format,
                    'has_transparency': img.mode in ('RGBA', 'LA') or 'transparency' in img.info
                })
                
                # EXIF data
                exif_data = img._getexif()
                if exif_data:
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, f"Unknown_{tag_id}")
                        # Convert complex objects to strings
                        if isinstance(value, (bytes, tuple)):
                            value = str(value)
                        metadata[f'exif_{tag}'] = value
                else:
                    metadata['exif_status'] = 'No EXIF data found'
                    
        except Exception as e:
            metadata['image_error'] = str(e)
        
        return metadata
    
    @staticmethod
    def extract_media_metadata(filepath: str) -> Dict[str, Any]:
        """Extract metadata from video/audio files"""
        if not MEDIAINFO_AVAILABLE:
            return {'error': 'pymediainfo not available'}
        
        metadata = {}
        try:
            media_info = MediaInfo.parse(filepath)
            
            for track in media_info.tracks:
                track_type = track.track_type.lower()
                track_data = track.to_data()
                
                # Add track-specific prefix
                for attr, val in track_data.items():
                    if val is not None and val != '':
                        key = f'{track_type}_{attr}'
                        metadata[key] = val
                        
        except Exception as e:
            metadata['media_error'] = str(e)
        
        return metadata
    
    @staticmethod
    def extract_all_metadata(filepath: str) -> Dict[str, Any]:
        """Extract comprehensive metadata from a file"""
        if not os.path.isfile(filepath):
            return {'error': f'File not found: {filepath}'}
        
        # Start with basic metadata
        metadata = MetadataExtractor.extract_basic_metadata(filepath)
        
        if 'error' in metadata:
            return metadata
        
        file_type = metadata.get('file_type', 'other')
        ext = metadata.get('extension', '').lower()
        
        # Extract type-specific metadata
        if file_type == 'image' and ext in IMAGE_EXTENSIONS:
            image_meta = MetadataExtractor.extract_image_metadata(filepath)
            metadata.update(image_meta)
        
        elif file_type in ['video', 'audio'] and (ext in VIDEO_EXTENSIONS or ext in AUDIO_EXTENSIONS):
            media_meta = MetadataExtractor.extract_media_metadata(filepath)
            metadata.update(media_meta)
        
        return metadata

class CSVManager:
    """Enhanced CSV management with better error handling"""
    
    @staticmethod
    def write_metadata_row(metadata: Dict[str, Any], csv_file_path: str) -> bool:
        """Write metadata to CSV file with improved error handling"""
        try:
            file_exists = os.path.isfile(csv_file_path)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
            
            with open(csv_file_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=metadata.keys())
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(metadata)
            return True
            
        except Exception as e:
            print(f"Error writing to CSV: {str(e)}")
            return False
    
    @staticmethod
    def export_to_json(metadata_list: List[Dict], json_file_path: str) -> bool:
        """Export metadata to JSON format"""
        try:
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(metadata_list, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error writing to JSON: {str(e)}")
            return False

class MetadataExtractorApp:
    """Enhanced GUI application with better UX and features"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Metadata Extractor v2.0 by @Tactical_Scientist")
        self.root.geometry("900x700")
        
        # Data storage
        self.processed_files = []
        self.current_metadata = []
        
        self.setup_menu()
        self.setup_widgets()
        self.setup_status_bar()
    
    def setup_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Files...", command=self.open_files)
        file_menu.add_separator()
        file_menu.add_command(label="Export to JSON...", command=self.export_json)
        file_menu.add_command(label="Clear Output", command=self.clear_output)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def setup_widgets(self):
        """Setup main application widgets"""
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Instructions
        instruction_frame = ttk.LabelFrame(main_frame, text="Instructions", padding=5)
        instruction_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(instruction_frame, 
                 text="Drag & drop files here, or use File > Open Files... to select files").pack(anchor=tk.W)
        
        # Processing options
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding=5)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.include_hash = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Include file hash (MD5)", 
                       variable=self.include_hash).pack(side=tk.LEFT)
        
        self.auto_export = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Auto-export to CSV", 
                       variable=self.auto_export).pack(side=tk.LEFT, padx=(20, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 5))
        
        # Output text area
        text_frame = ttk.LabelFrame(main_frame, text="Output", padding=5)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text = scrolledtext.ScrolledText(text_frame, width=100, height=25, 
                                            font=('Consolas', 9))
        self.text.pack(fill=tk.BOTH, expand=True)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Open Files", 
                  command=self.open_files).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Clear Output", 
                  command=self.clear_output).pack(side=tk.LEFT, padx=(5, 0))
        ttk.Button(button_frame, text="Export JSON", 
                  command=self.export_json).pack(side=tk.LEFT, padx=(5, 0))
        
        # Enable drag-and-drop
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)
    
    def setup_status_bar(self):
        """Setup status bar"""
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_status(self, message: str):
        """Update status bar message"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
    
    def on_drop(self, event):
        """Handle drag-and-drop files"""
        files = self.root.splitlist(event.data)
        self.process_files_async(files)
    
    def open_files(self):
        """Open file dialog to select files"""
        filetypes = [
            ("All files", "*.*"),
            ("Images", "*.jpg *.jpeg *.png *.tiff *.bmp *.gif *.webp"),
            ("Videos", "*.mp4 *.mov *.avi *.mkv *.flv *.wmv *.m4v *.webm"),
            ("Audio", "*.mp3 *.wav *.flac *.aac *.ogg *.wma *.m4a")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select files to extract metadata",
            filetypes=filetypes
        )
        
        if files:
            self.process_files_async(files)
    
    def process_files_async(self, file_list):
        """Process files in background thread"""
        threading.Thread(target=self.process_files, args=(file_list,), daemon=True).start()
    
    def process_files(self, file_list):
        """Process multiple files and extract metadata"""
        self.root.after(0, lambda: self.progress.start())
        self.root.after(0, lambda: self.update_status("Processing files..."))
        
        total_files = len(file_list)
        processed = 0
        
        for filepath in file_list:
            # Clean filepath (remove braces if present)
            filepath = filepath.strip('{}').strip('"').strip("'")
            
            if not os.path.isfile(filepath):
                self.root.after(0, lambda f=filepath: self.log_message(f"Skipped: {f} (not a file)\n"))
                continue
            
            processed += 1
            self.root.after(0, lambda p=processed, t=total_files: 
                          self.update_status(f"Processing file {p}/{t}..."))
            
            # Extract metadata
            metadata = MetadataExtractor.extract_all_metadata(filepath)
            
            if 'error' in metadata:
                self.root.after(0, lambda f=filepath, e=metadata['error']: 
                              self.log_message(f"Error processing {f}: {e}\n"))
                continue
            
            # Store metadata
            self.current_metadata.append(metadata)
            self.processed_files.append(filepath)
            
            # Display results
            self.root.after(0, lambda m=metadata: self.display_metadata(m))
            
            # Auto-export to CSV if enabled
            if self.auto_export.get():
                folder = os.path.dirname(os.path.abspath(filepath))
                csv_path = os.path.join(folder, 'metadata_output.csv')
                CSVManager.write_metadata_row(metadata, csv_path)
        
        self.root.after(0, lambda: self.progress.stop())
        self.root.after(0, lambda: self.update_status(f"Completed processing {processed} files"))
    
    def display_metadata(self, metadata: Dict[str, Any]):
        """Display metadata in the text widget"""
        filename = metadata.get('filename', 'Unknown')
        
        self.text.insert(tk.END, f"{'='*60}\n")
        self.text.insert(tk.END, f"METADATA FOR: {filename}\n")
        self.text.insert(tk.END, f"{'='*60}\n")
        
        # Group metadata by category
        categories = {
            'File Info': [],
            'Image Data': [],
            'Media Data': [],
            'EXIF Data': [],
            'Other': []
        }
        
        for key, value in metadata.items():
            if key.startswith('exif_'):
                categories['EXIF Data'].append((key, value))
            elif key.startswith(('image_', 'video_', 'audio_', 'general_')):
                categories['Media Data'].append((key, value))
            elif key in ['filename', 'filepath', 'size_bytes', 'size_mb', 'file_type', 'extension']:
                categories['File Info'].append((key, value))
            else:
                categories['Other'].append((key, value))
        
        # Display by category
        for category, items in categories.items():
            if items:
                self.text.insert(tk.END, f"\n[{category}]\n")
                for key, value in sorted(items):
                    self.text.insert(tk.END, f"  {key}: {value}\n")
        
        self.text.insert(tk.END, "\n")
        self.text.see(tk.END)
    
    def log_message(self, message: str):
        """Log a message to the text widget"""
        self.text.insert(tk.END, message)
        self.text.see(tk.END)
    
    def clear_output(self):
        """Clear the output text widget"""
        self.text.delete(1.0, tk.END)
        self.current_metadata.clear()
        self.processed_files.clear()
        self.update_status("Output cleared")
    
    def export_json(self):
        """Export current metadata to JSON file"""
        if not self.current_metadata:
            messagebox.showwarning("No Data", "No metadata to export. Process some files first.")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export metadata to JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            if CSVManager.export_to_json(self.current_metadata, filename):
                messagebox.showinfo("Success", f"Metadata exported to {filename}")
                self.update_status(f"Exported to {filename}")
            else:
                messagebox.showerror("Error", "Failed to export metadata")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Enhanced Metadata Extractor v2.0
        
Created by @Tactical_Scientist

Features:
• Drag & drop support for multiple files
• Comprehensive metadata extraction for images, videos, and audio
• Export to CSV and JSON formats
• File hash calculation for integrity verification
• Enhanced error handling and user interface

Supported formats:
• Images: JPG, PNG, TIFF, BMP, GIF, WebP
• Videos: MP4, MOV, AVI, MKV, FLV, WMV, M4V, WebM
• Audio: MP3, WAV, FLAC, AAC, OGG, WMA, M4A

Dependencies:
• tkinterdnd2: Drag & drop support
• Pillow (PIL): Image metadata extraction
• pymediainfo: Video/audio metadata extraction"""
        
        messagebox.showinfo("About", about_text)

def check_dependencies():
    """Check and report missing dependencies"""
    missing = []
    
    try:
        import tkinterdnd2
    except ImportError:
        missing.append("tkinterdnd2")
    
    if not PIL_AVAILABLE:
        missing.append("Pillow")
    
    if not MEDIAINFO_AVAILABLE:
        missing.append("pymediainfo")
    
    if missing:
        deps = ", ".join(missing)
        message = f"Missing dependencies: {deps}\n\nInstall with:\npip install {' '.join(missing)}"
        messagebox.showerror("Missing Dependencies", message)
        return False
    
    return True

def main():
    """Main application entry point"""
    if not check_dependencies():
        return
    
    root = TkinterDnD.Tk()
    app = MetadataExtractorApp(root)
    
    # Set window icon (if available)
    try:
        root.iconbitmap("icon.ico")  # Add your icon file
    except:
        pass
    
    root.mainloop()

if __name__ == "__main__":
    main()