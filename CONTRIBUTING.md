# Contributing

Terima kasih atas minatmu! Repo ini adalah proyek portofolio kecil, tetapi
kontribusi tetap diterima.

## Menjalankan proyek secara lokal

```bash
git clone https://github.com/muhammaddani/csv-report-cli.git
cd csv-report-cli
pip install -r requirements.txt   # opsional, hanya untuk ekspor Excel
pip install pytest
pytest -v
```

## Alur kontribusi

1. Buat branch baru: `git checkout -b feat/nama-fitur`
2. Tulis kode dan **tambahkan test** untuk perubahan tersebut.
3. Pastikan semua test lulus: `pytest -v`
4. Commit dengan pesan yang jelas (lihat gaya di bawah).
5. Buka Pull Request.

## Gaya commit

Mengikuti pola konvensional:

- `feat: ...` — fitur baru
- `fix: ...` — perbaikan bug
- `docs: ...` — perubahan dokumentasi
- `test: ...` — menambah atau memperbaiki test
- `chore: ...` — pekerjaan rumah tangga

## Prinsip

- Satu perubahan, satu tujuan.
- Setiap perubahan perilaku harus disertai test.
- Jaga agar kode mudah dibaca; kejelasan lebih penting daripada keringkasan.