# Digital-Forensic-Tools-Development-Projects-01-Metadata-Extractor-For-Windows
## Metadata Extractor Version 1

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Aplikasi desktop berbasis GUI untuk mengekstrak metadata dari file gambar dan video/audio dengan fitur drag-and-drop yang mudah digunakan.

## 🌟 Fitur

- **Drag & Drop Interface**: Seret dan lepas file langsung ke aplikasi
- **Multi-format Support**: 
  - Gambar: JPG, JPEG, TIFF, PNG
  - Video: MP4, MOV, AVI, MKV
  - Audio: MP3, WAV
- **EXIF Data Extraction**: Ekstrak data EXIF lengkap dari file gambar
- **Media Information**: Dapatkan informasi detail dari file video dan audio
- **Auto CSV Export**: Metadata otomatis disimpan ke file CSV di folder yang sama dengan file sumber
- **Real-time Display**: Tampilan metadata langsung di aplikasi
- **Multi-threading**: Pemrosesan file di background untuk menjaga UI tetap responsif

## 📋 Prerequisites

- Python 3.7 atau lebih tinggi
- pip (Python package manager)

## 🔧 Instalasi

1. **Clone repository** (atau download source code):
```bash
git clone <repository-url>
cd metadata-extractor
```

2. **Install dependencies**:
```bash
pip install tkinterdnd2 pillow pymediainfo
```

### Dependensi yang Dibutuhkan:
- `tkinterdnd2`: Library untuk drag-and-drop functionality
- `pillow`: Library untuk pemrosesan gambar dan ekstraksi EXIF
- `pymediainfo`: Library untuk ekstraksi metadata video/audio

### Catatan untuk Windows:
Untuk `pymediainfo`, Anda mungkin perlu menginstall MediaInfo library secara terpisah:
1. Download MediaInfo dari [mediaarea.net](https://mediaarea.net/en/MediaInfo/Download)
2. Install dan pastikan tersedia di system PATH

### Catatan untuk Linux:
```bash
sudo apt-get install libmediainfo-dev
pip install tkinterdnd2 pillow pymediainfo
```

### Catatan untuk macOS:
```bash
brew install media-info
pip install tkinterdnd2 pillow pymediainfo
```

## 🚀 Cara Penggunaan

1. **Jalankan aplikasi**:
```bash
python metadata_extractor.py
```

2. **Ekstrak metadata**:
   - Seret file gambar atau video ke jendela aplikasi
   - Metadata akan langsung ditampilkan di area teks
   - File CSV akan otomatis dibuat di folder yang sama dengan nama `metadata_output.csv`

3. **Output CSV**:
   - Setiap file yang diproses akan menambahkan baris baru ke CSV
   - CSV berisi semua metadata yang diekstrak
   - File CSV dibuat di folder yang sama dengan file sumber

## 📊 Metadata yang Diekstrak

### Informasi File Dasar:
- Nama file
- Path lengkap
- Ukuran file (bytes)
- Tanggal dibuat
- Tanggal dimodifikasi

### Data EXIF (untuk gambar):
- Model kamera
- Tanggal pengambilan foto
- Resolusi
- ISO, aperture, shutter speed
- GPS coordinates (jika tersedia)
- Dan banyak lagi...

### Media Info (untuk video/audio):
- Codec video/audio
- Bitrate
- Frame rate
- Durasi
- Resolusi
- Format container
- Dan metadata lainnya...

## 📁 Struktur Output

```
/path/to/your/files/
├── your_image.jpg
├── your_video.mp4
└── metadata_output.csv  ← File CSV dibuat otomatis di sini
```

## 🔍 Contoh Output CSV

| filename | filepath | size_bytes | created | modified | exif_Make | exif_Model | ... |
|----------|----------|------------|---------|----------|-----------|------------|-----|
| photo.jpg | /path/to/photo.jpg | 2456789 | 2024-01-15T10:30:00 | 2024-01-15T10:30:00 | Canon | EOS 5D | ... |

## ⚠️ Troubleshooting

### Error: "Please install tkinterdnd2"
```bash
pip install tkinterdnd2
```

### Error: "MediaInfo library not found"
- **Windows**: Download dan install MediaInfo dari website resmi
- **Linux**: `sudo apt-get install libmediainfo-dev`
- **macOS**: `brew install media-info`

### UI tidak responsif saat memproses banyak file
Aplikasi menggunakan threading untuk menjaga UI tetap responsif. Jika masalah terjadi, proses file dalam batch yang lebih kecil.

## 🤝 Kontribusi

Kontribusi selalu diterima! Silakan:
1. Fork repository
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📝 License

Project ini menggunakan MIT License - lihat file LICENSE untuk detail.

## 👨‍💻 Author

**@Tactical_Scientist**

## 🙏 Acknowledgments

- [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2) - Drag and drop support
- [Pillow](https://python-pillow.org/) - Image processing
- [pymediainfo](https://pymediainfo.readthedocs.io/) - Media metadata extraction

## 📮 Support

Jika Anda menemukan bug atau memiliki saran, silakan buat issue di repository ini.

---

Made with ❤️ by @Tactical_Scientist
