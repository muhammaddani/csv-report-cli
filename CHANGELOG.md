# Changelog

Semua perubahan penting pada proyek ini didokumentasikan di file ini.

Format mengikuti [Keep a Changelog](https://keepachangelog.com/) dan proyek ini
menganut [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-11-23

### Ditambahkan
- CLI untuk membaca CSV penjualan dan mencetak laporan ringkasan.
- Ringkasan total pendapatan, total unit, dan jumlah transaksi.
- Agregasi pendapatan per produk dan per wilayah.
- Deteksi produk terlaris.
- Ekspor laporan ke Excel multi-sheet (opsional, via `--excel`).
- Penanganan baris CSV rusak tanpa menggagalkan seluruh laporan.
- 12 test otomatis (pytest).
- CI GitHub Actions pada Python 3.10–3.12.
- `Makefile`, `CONTRIBUTING.md`, dan `pyproject.toml`.

### Diperbaiki
- Pesan error yang jelas saat `openpyxl` belum terpasang (sebelumnya crash
  dengan stack trace).