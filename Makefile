.PHONY: help install test lint clean run excel

help:  ## Tampilkan daftar perintah
	@echo "Perintah yang tersedia:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  make %-12s %s\n", $$1, $$2}'

install:  ## Pasang dependensi (termasuk pytest)
	python -m pip install --upgrade pip
	pip install -r requirements.txt pytest

test:  ## Jalankan seluruh test
	pytest -v

run:  ## Jalankan contoh laporan pada data sampel
	python src/report.py data/sales_sample.csv

excel:  ## Buat contoh laporan Excel
	python src/report.py data/sales_sample.csv --excel out/laporan.xlsx

clean:  ## Hapus artefak cache dan keluaran
	rm -rf out .pytest_cache __pycache__ src/__pycache__ tests/__pycache__
	find . -name "*.pyc" -delete