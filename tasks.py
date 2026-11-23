#!/usr/bin/env python3
"""Tugas pengembangan lintas-platform untuk csv-report-cli.

Dipakai agar perintah umum bisa dijalankan di Windows, Linux, dan macOS
tanpa perlu `make`. Tidak butuh dependensi eksternal.

Contoh:
    python tasks.py            # tampilkan daftar tugas
    python tasks.py test       # jalankan test
    python tasks.py run        # contoh laporan
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _run(cmd: list[str]) -> int:
    print("$", " ".join(cmd))
    return subprocess.call(cmd, cwd=ROOT)


def install() -> int:
    """Pasang dependensi (pytest + dependensi Excel)."""
    code = _run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    if code:
        return code
    return _run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "pytest"])


def test() -> int:
    """Jalankan seluruh test."""
    return _run([sys.executable, "-m", "pytest", "-v"])


def run() -> int:
    """Jalankan laporan contoh pada data sampel."""
    return _run([sys.executable, "src/report.py", "data/sales_sample.csv"])


def excel() -> int:
    """Buat contoh laporan Excel."""
    return _run(
        [sys.executable, "src/report.py", "data/sales_sample.csv", "--excel", "out/laporan.xlsx"]
    )


def clean() -> int:
    """Hapus artefak cache dan keluaran."""
    for target in [".pytest_cache", "__pycache__", "src/__pycache__", "tests/__pycache__"]:
        shutil.rmtree(ROOT / target, ignore_errors=True)
    for pyc in ROOT.rglob("*.pyc"):
        pyc.unlink(missing_ok=True)
    shutil.rmtree(ROOT / "out", ignore_errors=True)
    print("Bersih.")
    return 0


TASKS = {
    "install": (install, "Pasang dependensi (pytest + Excel)"),
    "test": (test, "Jalankan seluruh test"),
    "run": (run, "Contoh laporan pada data sampel"),
    "excel": (excel, "Buat contoh laporan Excel"),
    "clean": (clean, "Hapus cache dan keluaran"),
}


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in {"-h", "--help", "help"}:
        print("Tugas yang tersedia:\n")
        for name, (_, desc) in TASKS.items():
            print(f"  python tasks.py {name:<8} {desc}")
        return 0

    name = sys.argv[1]
    if name not in TASKS:
        print(f"Tugas tidak dikenal: {name}", file=sys.stderr)
        return 1
    return TASKS[name][0]()


if __name__ == "__main__":
    raise SystemExit(main())