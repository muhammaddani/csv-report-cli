# csv-report-cli

[![CI](https://github.com/muhammaddani/csv-report-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/muhammaddani/csv-report-cli/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

Alat baris perintah (CLI) untuk mengubah file **CSV penjualan mentah** menjadi
**laporan ringkasan** yang langsung terbaca di terminal, dan opsional diekspor
ke **Excel**.

Dibuat untuk kasus yang sangat umum di UMKM dan tim kecil: data penjualan ada di
file CSV, tetapi untuk tahu "produk mana yang paling laku" atau "wilayah mana
yang paling untung", orang masih menghitungnya manual di spreadsheet.

## Fitur

- Ringkasan total pendapatan, total unit, dan jumlah transaksi
- Pendapatan per produk (diurutkan dari terbesar)
- Pendapatan per wilayah (region)
- Produk terlaris berdasarkan jumlah unit
- Ekspor ke Excel multi-sheet (opsional)
- Baris CSV yang rusak dilewati dengan peringatan, tidak menggagalkan seluruh laporan
- Pesan error yang jelas jika file tidak ada atau format kolom salah

## Kebutuhan

- Python 3.10+ (logika inti hanya memakai standard library)
- Opsional, untuk ekspor Excel: `pandas` dan `openpyxl`

## Instalasi

```bash
# Logika inti tidak butuh apa pun selain Python.
# Untuk fitur ekspor Excel, pasang dependensi opsional:
pip install -r requirements.txt
```

## Cara pakai

```bash
# Laporan ringkasan di terminal
python src/report.py data/sales_sample.csv

# Laporan + ekspor ke Excel
python src/report.py data/sales_sample.csv --excel out/laporan.xlsx
```

### Contoh keluaran

```
====================================================
  LAPORAN PENJUALAN
====================================================
  Jumlah transaksi : 12
  Total unit       : 170
  Total pendapatan : Rp 6.227.000

  Pendapatan per produk
  ------------------------------------------------
    - Kopi Arabika         Rp 3.015.000
    - Kopi Robusta         Rp 1.862.000
    - Teh Hijau            Rp 1.350.000

  Pendapatan per wilayah
  ------------------------------------------------
    - Surabaya             Rp 2.895.000
    - Jakarta              Rp 2.170.000
    - Bandung              Rp 1.162.000

  Produk terlaris  : Kopi Arabika (67 unit)
====================================================
```

## Format CSV yang diharapkan

File CSV harus memiliki baris header dengan kolom berikut:

| Kolom        | Tipe    | Keterangan                       |
|--------------|---------|----------------------------------|
| `date`       | teks    | Tanggal transaksi (bebas format) |
| `product`    | teks    | Nama produk                      |
| `region`     | teks    | Wilayah penjualan                |
| `quantity`   | angka   | Jumlah unit terjual              |
| `unit_price` | angka   | Harga satuan                     |

Contoh ada di [`data/sales_sample.csv`](data/sales_sample.csv).

## Struktur proyek

```
csv-report-cli/
├── src/
│   └── report.py          # seluruh logika program + CLI
├── tests/
│   └── test_report.py     # test otomatis (pytest)
├── data/
│   └── sales_sample.csv   # data contoh
├── .github/workflows/
│   └── ci.yml             # CI: jalankan test di setiap push
├── requirements.txt       # dependensi opsional (Excel export)
├── LICENSE                # lisensi MIT
└── README.md
```

## Menjalankan test

```bash
pip install pytest
pytest -v
```

Test mencakup pembacaan CSV, validasi kolom, penanganan baris rusak, agregasi
laporan, dan format mata uang. CI menjalankannya otomatis pada Python 3.10–3.12
setiap kali ada push.

## Ide pengembangan lanjutan

- Filter berdasarkan rentang tanggal
- Ringkasan per bulan
- Format keluaran JSON / Markdown
- Mode pengawasan folder (otomatis lapor saat ada CSV baru)

## Lisensi

MIT — lihat [LICENSE](LICENSE).