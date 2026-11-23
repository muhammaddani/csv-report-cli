# justfile -- alternatif ringkas jika kamu memakai `just`
# (https://github.com/casey/just). Pengguna Windows tanpa `just` bisa
# memakai `python tasks.py <tugas>`.

default:
    @just --list

install:
    python -m pip install --upgrade pip
    pip install -r requirements.txt pytest

test:
    pytest -v

run:
    python src/report.py data/sales_sample.csv

excel:
    python src/report.py data/sales_sample.csv --excel out/laporan.xlsx

clean:
    python tasks.py clean