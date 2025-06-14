# Metadata-Extractor Versi Deployement Ke Github

import os
import csv
import datetime
import threading
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
except ImportError:
    raise ImportError("Please install tkinterdnd2: pip install tkinterdnd2")
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from PIL import Image
from PIL.ExifTags import TAGS
from pymediainfo import MediaInfo

# CSV output file
def write_csv_row(row, csv_file_path):
    """
    Tulis satu baris metadata ke file CSV di path yang diberikan.
    Jika file belum ada, header akan ditulis terlebih dahulu.
    """
    file_exists = os.path.isfile(csv_file_path)
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

# Metadata extraction functions
def extract_file_metadata(filepath):
    metadata = {
        'filename': os.path.basename(filepath),
        'filepath': os.path.abspath(filepath),
        'size_bytes': os.path.getsize(filepath),
        'created': datetime.datetime.fromtimestamp(os.path.getctime(filepath)).isoformat(),
        'modified': datetime.datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat(),
    }
    ext = os.path.splitext(filepath)[1].lower()
    # Image EXIF
    if ext in ['.jpg', '.jpeg', '.tiff', '.png']:
        try:
            img = Image.open(filepath)
            exif_data = img._getexif() or {}
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                metadata[f'exif_{tag}'] = value
        except Exception as e:
            metadata['exif_error'] = str(e)
    # Video/audio metadata
    if ext in ['.mp4', '.mov', '.avi', '.mkv', '.mp3', '.wav']:
        try:
            media_info = MediaInfo.parse(filepath)
            for track in media_info.tracks:
                prefix = track.track_type.lower()
                for attr, val in track.to_data().items():
                    metadata[f'{prefix}_{attr}'] = val
        except Exception as e:
            metadata['mediainfo_error'] = str(e)
    return metadata

# GUI Application

def process_files(file_list, text_widget):
    for filepath in file_list:
        filepath = filepath.strip('{ }')  # remove braces
        if not os.path.isfile(filepath):
            continue
        # Extract metadata
        metadata = extract_file_metadata(filepath)
        # Display in text widget
        text_widget.insert(tk.END, f"Metadata for {metadata['filename']}:\n")
        for k, v in metadata.items():
            text_widget.insert(tk.END, f"  {k}: {v}\n")
        text_widget.insert(tk.END, "\n")
        text_widget.see(tk.END)
        # Tentukan lokasi CSV di folder file
        folder = os.path.dirname(os.path.abspath(filepath))
        csv_path = os.path.join(folder, 'metadata_output.csv')
        # Tulis metadata ke CSV di folder yang sama
        write_csv_row(metadata, csv_path)

class MetadataExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Metadata Extractor by @Tactical_Scientist")
        self.setup_widgets()

    def setup_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        label = ttk.Label(frame, text="Drag & drop files yang akan ditampilkan Metadata:")
        label.pack(anchor=tk.W)

        self.text = scrolledtext.ScrolledText(frame, width=80, height=20)
        self.text.pack(fill=tk.BOTH, expand=True, pady=5)

        # Enable drag-and-drop
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)

    def on_drop(self, event):
        files = self.root.splitlist(event.data)
        # Process in background thread to keep UI responsive
        threading.Thread(target=process_files, args=(files, self.text), daemon=True).start()

if __name__ == "__main__":
    # Check dependencies
    try:
        import tkinterdnd2
    except ImportError:
        messagebox.showerror("Missing Dependency", "Please install dependencies: pip install tkinterdnd2 pillow pymediainfo")
        exit(1)

    root = TkinterDnD.Tk()
    app = MetadataExtractorApp(root)
    root.mainloop()
