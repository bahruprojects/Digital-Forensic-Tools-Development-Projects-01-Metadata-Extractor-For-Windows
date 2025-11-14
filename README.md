# Digital-Forensic-Tools-Development-Projects-01-Metadata-Extractor-For-Windows
## Metadata Extractor Version 2

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Version](https://img.shields.io/badge/Version-2.0-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Aplikasi desktop berbasis GUI yang powerful untuk mengekstrak metadata komprehensif dari berbagai jenis file dengan antarmuka drag-and-drop yang intuitif dan fitur-fitur canggih.

## ✨ Fitur Unggulan

### 🎯 Core Features
- **Drag & Drop Interface**: Seret dan lepas file langsung ke aplikasi untuk pemrosesan instant
- **Batch Processing**: Proses multiple files sekaligus dengan multi-threading
- **Multi-format Support**: Mendukung 20+ format file populer
- **Dual Export**: Export otomatis ke CSV dan JSON
- **File Integrity**: Kalkulasi hash MD5 untuk verifikasi integritas file
- **Real-time Progress**: Progress bar dan status updates yang informatif

### 📊 Format File yang Didukung
- **Gambar**: JPG, JPEG, PNG, TIFF, TIF, BMP, GIF, WebP
- **Video**: MP4, MOV, AVI, MKV, FLV, WMV, M4V, WebM
- **Audio**: MP3, WAV, FLAC, AAC, OGG, WMA, M4A
- **Dokumen**: PDF, DOC, DOCX, TXT, RTF (metadata dasar)

### 🔍 Metadata yang Diekstrak

#### File Information (Semua file)
- Nama file dan path lengkap
- Direktori lokasi
- Ekstensi dan tipe file
- Ukuran (bytes dan MB)
- Timestamps (created, modified, accessed)
- File permissions
- MD5 hash untuk verifikasi integritas
- Timestamp ekstraksi metadata

#### Image Metadata (EXIF)
- Dimensi (width × height)
- Mode dan format gambar
- Status transparansi
- Data EXIF lengkap:
  - Model kamera dan lensa
  - Settings foto (ISO, aperture, shutter speed)
  - Tanggal dan waktu pengambilan
  - GPS coordinates (jika tersedia)
  - White balance, flash, focal length
  - Dan 50+ field EXIF lainnya

#### Video/Audio Metadata
- Codec video dan audio
- Bitrate dan sample rate
- Frame rate dan resolusi
- Durasi media
- Format container
- Channel layout
- Track information
- Dan banyak technical details lainnya

## 📋 Prerequisites

- **Python**: 3.7 atau lebih tinggi
- **pip**: Python package manager
- **Sistem Operasi**: Windows, Linux, atau macOS

## 🔧 Instalasi

### 1. Clone/Download Repository
```bash
git clone <repository-url>
cd metadata-extractor
```

### 2. Install Dependencies

#### Instalasi Lengkap (Recommended)
```bash
pip install tkinterdnd2 pillow pymediainfo
```

#### Instalasi Per Komponen
```bash
# Core dependency (wajib)
pip install tkinterdnd2

# Image support (opsional, untuk ekstraksi EXIF)
pip install pillow

# Media support (opsional, untuk video/audio)
pip install pymediainfo
```

### 3. Install MediaInfo Library (untuk pymediainfo)

#### Windows
1. Download MediaInfo dari [mediaarea.net/en/MediaInfo/Download](https://mediaarea.net/en/MediaInfo/Download)
2. Install executable yang sesuai dengan sistem Anda
3. Pastikan MediaInfo tersedia di system PATH

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install libmediainfo-dev
```

#### Linux (Fedora/RHEL)
```bash
sudo dnf install mediainfo-devel
```

#### macOS
```bash
brew install media-info
```

## 🚀 Cara Penggunaan

### Menjalankan Aplikasi
```bash
python metadata_extractor.py
```

### Metode 1: Drag & Drop
1. Buka aplikasi
2. Seret file dari Windows Explorer/Finder
3. Lepas file di jendela aplikasi
4. Metadata akan otomatis diekstrak dan ditampilkan

### Metode 2: File Dialog
1. Klik menu **File → Open Files...**
2. Pilih satu atau lebih file dari dialog
3. Klik **Open** untuk memproses

### Opsi Pengaturan

#### Include File Hash (MD5)
- ✅ **Enabled**: Hitung MD5 hash untuk setiap file (default)
- ❌ **Disabled**: Skip hash calculation untuk proses lebih cepat

#### Auto-export to CSV
- ✅ **Enabled**: Otomatis export ke CSV setiap file diproses (default)
- ❌ **Disabled**: Hanya tampilkan di aplikasi tanpa export

### Export Data

#### CSV Export (Otomatis)
File `metadata_output.csv` dibuat otomatis di folder yang sama dengan file sumber:
```
/path/to/your/files/
├── photo1.jpg
├── photo2.jpg
├── video.mp4
└── metadata_output.csv  ← Auto-generated
```

#### JSON Export (Manual)
1. Process beberapa file
2. Klik menu **File → Export to JSON...**
3. Pilih lokasi dan nama file
4. Semua metadata dari sesi saat ini akan di-export

## 📁 Struktur Output

### CSV Format
File CSV berisi semua metadata dalam format tabular dengan headers dinamis sesuai dengan field yang tersedia:

| filename | filepath | size_mb | file_type | md5_hash | exif_Make | exif_Model | video_duration | ... |
|----------|----------|---------|-----------|----------|-----------|------------|----------------|-----|
| photo.jpg | /path/to/photo.jpg | 2.34 | image | a1b2c3... | Canon | EOS 5D | - | ... |
| video.mp4 | /path/to/video.mp4 | 45.67 | video | d4e5f6... | - | - | 00:05:30 | ... |

### JSON Format
```json
[
  {
    "filename": "photo.jpg",
    "filepath": "/path/to/photo.jpg",
    "file_type": "image",
    "size_mb": 2.34,
    "md5_hash": "a1b2c3d4e5f6...",
    "image_width": 1920,
    "image_height": 1080,
    "exif_Make": "Canon",
    "exif_Model": "EOS 5D",
    "exif_DateTime": "2024:01:15 10:30:00",
    ...
  }
]
```

## 🎨 Antarmuka Pengguna

### Menu Bar
- **File**
  - Open Files... (Ctrl+O): Buka file dialog
  - Export to JSON...: Export metadata ke JSON
  - Clear Output: Bersihkan tampilan output
  - Exit: Keluar dari aplikasi
- **Help**
  - About: Informasi tentang aplikasi

### Main Window
- **Instructions Panel**: Panduan penggunaan
- **Options Panel**: Checkbox untuk konfigurasi
- **Progress Bar**: Indikator pemrosesan file
- **Output Area**: Display metadata yang diekstrak
- **Control Buttons**: Quick access ke fungsi utama
- **Status Bar**: Status dan notifikasi real-time

## ⚙️ Konfigurasi Lanjutan

### Menambah Format File Baru
Edit konstanta di bagian atas kode:
```python
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', ...}
VIDEO_EXTENSIONS = {'.mp4', '.mov', ...}
AUDIO_EXTENSIONS = {'.mp3', '.wav', ...}
```

### Mengubah Hash Algorithm
Modify method `calculate_file_hash`:
```python
# Gunakan SHA256 instead of MD5
hash_obj = hashlib.new('sha256')
```

### Custom CSV Output Path
Modify di method `process_files`:
```python
csv_path = os.path.join(folder, 'custom_metadata.csv')
```

## 🐛 Troubleshooting

### Error: "Please install tkinterdnd2"
**Solusi:**
```bash
pip install tkinterdnd2
```

### Error: "PIL/Pillow not available"
**Solusi:**
```bash
pip install pillow
```
Aplikasi tetap bisa jalan, tapi ekstraksi metadata gambar akan di-disable.

### Error: "pymediainfo not available"
**Solusi:**
```bash
# Install pymediainfo
pip install pymediainfo

# Install MediaInfo library
# Windows: Download dari mediaarea.net
# Linux: sudo apt-get install libmediainfo-dev
# macOS: brew install media-info
```

### Error: "MediaInfo library not found"
Pastikan MediaInfo library sudah terinstall di sistem (lihat bagian Instalasi).

### UI Freeze saat Processing
Aplikasi menggunakan multi-threading, tapi untuk file sangat besar:
- Proses file dalam batch yang lebih kecil
- Disable hash calculation untuk speedup
- Gunakan SSD untuk performa optimal

### Metadata Tidak Lengkap
Beberapa file mungkin tidak memiliki metadata lengkap:
- File yang baru dibuat tanpa metadata EXIF
- File yang sudah di-strip metadata-nya
- Format file yang tidak standar

### Permission Error
Pastikan Anda memiliki read permission untuk file yang diproses:
```bash
# Linux/macOS
chmod +r filename

# Windows: Properties → Security → Edit permissions
```

## 🔒 Keamanan dan Privacy

- **Local Processing**: Semua ekstraksi dilakukan secara lokal, tidak ada data yang dikirim ke server
- **Hash Verification**: MD5 hash membantu memverifikasi integritas file
- **Privacy Notice**: Metadata EXIF dapat mengandung informasi sensitif (GPS location, device info)
- **Recommendation**: Periksa metadata sebelum sharing file secara publik

## 🚀 Performance Tips

1. **Batch Processing**: Process multiple files sekaligus untuk efisiensi
2. **Disable Hash**: Turn off MD5 calculation untuk file besar jika tidak diperlukan
3. **SSD Storage**: Proses file dari SSD untuk I/O lebih cepat
4. **Close Other Apps**: Free up RAM untuk processing files yang besar

## 🤝 Kontribusi

Kontribusi sangat diterima! Cara berkontribusi:

1. Fork repository ini
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

### Guidelines
- Ikuti Python PEP 8 style guide
- Tambahkan docstrings untuk fungsi baru
- Test di Windows, Linux, dan macOS jika memungkinkan
- Update README jika menambah fitur baru

## 📝 Changelog

### Version 2.0 (Current)
- ✨ Enhanced UI dengan menu bar dan status bar
- ✨ JSON export functionality
- ✨ File hash calculation (MD5)
- ✨ Improved error handling dan logging
- ✨ Kategorisasi metadata yang lebih baik
- ✨ File dialog untuk pemilihan file
- ✨ Progress indicators
- ✨ Configurable options (hash, auto-export)
- 🐛 Bug fixes dan stability improvements

### Version 1.0
- Basic drag & drop functionality
- CSV export
- EXIF and media metadata extraction

## 📄 License

Project ini menggunakan MIT License. Lihat file [LICENSE](LICENSE) untuk detail lengkap.

```
MIT License

Copyright (c) 2024 @Tactical_Scientist

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

## 👨‍💻 Author

**@Tactical_Scientist**

## 🙏 Acknowledgments

Terima kasih kepada developer dan maintainer dari:

- **[tkinterdnd2](https://github.com/pmgagne/tkinterdnd2)** - Drag and drop functionality
- **[Pillow](https://python-pillow.org/)** - Powerful image processing library
- **[pymediainfo](https://pymediainfo.readthedocs.io/)** - Comprehensive media metadata extraction
- **[MediaInfo](https://mediaarea.net/)** - Multimedia file analysis tool

## 📮 Support & Feedback

Jika Anda menemukan bug atau memiliki saran:

1. **Bug Reports**: Buat issue di GitHub dengan label "bug"
2. **Feature Requests**: Buat issue dengan label "enhancement"
3. **Questions**: Buka discussion di GitHub Discussions
4. **Security Issues**: Email langsung ke Rahmikalfin@gmail.com

## 🌟 Star History

Jika project ini berguna untuk Anda, consider memberikan ⭐ di GitHub!

---

**Made with ❤️ by @Tactical_Scientist**

*Empowering digital forensics and media management, one metadata at a time.*
