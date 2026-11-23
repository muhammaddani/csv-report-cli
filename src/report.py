#!/usr/bin/env python3
"""
csv-report-cli
==============

Mengubah file CSV mentah berisi data penjualan menjadi laporan ringkasan
yang mudah dibaca, langsung di terminal.

Cara pakai singkat:
    python src/report.py data/sales_sample.csv

Fitur:
    - Ringkasan total pendapatan, total unit, dan jumlah transaksi
    - Pendapatan per produk
    - Pendapatan per wilayah (region)
    - Produk terlaris
    - Ekspor hasil ke Excel (.xlsx) -- opsional, butuh pandas + openpyxl

Program ini sengaja hanya memakai standard library untuk logikanya,
supaya bisa dijalankan di mana saja tanpa instalasi tambahan.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Model data
# ---------------------------------------------------------------------------

@dataclass
class Transaction:
    """Satu baris transaksi penjualan yang sudah divalidasi."""

    date: str
    product: str
    region: str
    quantity: int
    unit_price: float

    @property
    def revenue(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class Report:
    """Hasil agregasi seluruh transaksi."""

    transactions: list[Transaction] = field(default_factory=list)
    revenue_by_product: dict[str, float] = field(default_factory=lambda: defaultdict(float))
    quantity_by_product: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    revenue_by_region: dict[str, float] = field(default_factory=lambda: defaultdict(float))

    @property
    def total_revenue(self) -> float:
        return sum(t.revenue for t in self.transactions)

    @property
    def total_units(self) -> int:
        return sum(t.quantity for t in self.transactions)

    @property
    def transaction_count(self) -> int:
        return len(self.transactions)

    @property
    def best_selling_product(self) -> tuple[str, int] | None:
        if not self.quantity_by_product:
            return None
        return max(self.quantity_by_product.items(), key=lambda item: item[1])


# ---------------------------------------------------------------------------
# Pembacaan & validasi CSV
# ---------------------------------------------------------------------------

REQUIRED_COLUMNS = {"date", "product", "region", "quantity", "unit_price"}


class CsvFormatError(Exception):
    """Dilempar saat struktur CSV tidak sesuai harapan."""


def parse_csv(path: Path) -> list[Transaction]:
    """Baca CSV dan kembalikan daftar Transaction yang valid.

    Baris yang rusak (misalnya quantity bukan angka) dilewati dan dicatat
    sebagai peringatan, supaya satu baris buruk tidak menggagalkan
    seluruh laporan.
    """

    if not path.exists():
        raise FileNotFoundError(f"File CSV tidak ditemukan: {path}")

    transactions: list[Transaction] = []
    skipped: list[tuple[int, str]] = []

    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)

        if reader.fieldnames is None:
            raise CsvFormatError("File CSV kosong atau tidak memiliki baris header.")

        missing = REQUIRED_COLUMNS - {name.strip() for name in reader.fieldnames}
        if missing:
            raise CsvFormatError(
                "Kolom wajib tidak ditemukan: " + ", ".join(sorted(missing))
            )

        for line_no, row in enumerate(reader, start=2):
            try:
                transactions.append(
                    Transaction(
                        date=(row["date"] or "").strip(),
                        product=(row["product"] or "").strip(),
                        region=(row["region"] or "").strip(),
                        quantity=int(float((row["quantity"] or "0").strip())),
                        unit_price=float((row["unit_price"] or "0").strip()),
                    )
                )
            except (ValueError, TypeError, AttributeError) as exc:
                skipped.append((line_no, str(exc)))

    if skipped:
        print(f"  ! {len(skipped)} baris dilewati karena data tidak valid:", file=sys.stderr)
        for line_no, reason in skipped:
            print(f"    - baris {line_no}: {reason}", file=sys.stderr)

    return transactions


def build_report(transactions: list[Transaction]) -> Report:
    """Agregasi transaksi menjadi struktur Report."""

    report = Report(transactions=transactions)
    for t in transactions:
        report.revenue_by_product[t.product] += t.revenue
        report.quantity_by_product[t.product] += t.quantity
        report.revenue_by_region[t.region] += t.revenue
    return report


# ---------------------------------------------------------------------------
# Format & tampilan
# ---------------------------------------------------------------------------

def format_currency(value: float) -> str:
    """Format angka sebagai Rupiah, mis. 1250000 -> 'Rp 1.250.000'."""

    return "Rp " + f"{value:,.0f}".replace(",", ".")


def print_report(report: Report) -> None:
    """Cetak laporan ringkas ke stdout."""

    line = "=" * 52
    print(line)
    print("  LAPORAN PENJUALAN")
    print(line)
    print(f"  Jumlah transaksi : {report.transaction_count}")
    print(f"  Total unit       : {report.total_units}")
    print(f"  Total pendapatan : {format_currency(report.total_revenue)}")

    print()
    print("  Pendapatan per produk")
    print("  " + "-" * 48)
    for product, revenue in sorted(
        report.revenue_by_product.items(), key=lambda item: item[1], reverse=True
    ):
        print(f"    - {product:<20} {format_currency(revenue)}")

    print()
    print("  Pendapatan per wilayah")
    print("  " + "-" * 48)
    for region, revenue in sorted(
        report.revenue_by_region.items(), key=lambda item: item[1], reverse=True
    ):
        print(f"    - {region:<20} {format_currency(revenue)}")

    best = report.best_selling_product
    if best:
        print()
        print(f"  Produk terlaris  : {best[0]} ({best[1]} unit)")

    print(line)


def export_excel(report: Report, destination: Path) -> None:
    """Ekspor laporan ke file Excel (.xlsx).

    Fungsi ini butuh pandas + openpyxl. Jika tidak terpasang, program
    memberi pesan yang jelas, bukan langsung crash.
    """

    try:
        import pandas as pd  # noqa: WPS433 (import lokal disengaja)
        import openpyxl  # noqa: F401,WPS433 (dicek agar errornya jelas)
    except ImportError:
        print(
            "\n  ! Ekspor Excel butuh pandas dan openpyxl.\n"
            "    Pasang dulu:  pip install -r requirements.txt",
            file=sys.stderr,
        )
        return

    rows = [
        {
            "date": t.date,
            "product": t.product,
            "region": t.region,
            "quantity": t.quantity,
            "unit_price": t.unit_price,
            "revenue": t.revenue,
        }
        for t in report.transactions
    ]

    with pd.ExcelWriter(destination, engine="openpyxl") as writer:
        pd.DataFrame(rows).to_excel(writer, sheet_name="Transaksi", index=False)

        summary = pd.DataFrame(
            {
                "Metrik": ["Jumlah transaksi", "Total unit", "Total pendapatan"],
                "Nilai": [
                    report.transaction_count,
                    report.total_units,
                    report.total_revenue,
                ],
            }
        )
        summary.to_excel(writer, sheet_name="Ringkasan", index=False)

        pd.DataFrame(
            [
                {"Produk": k, "Pendapatan": v}
                for k, v in report.revenue_by_product.items()
            ]
        ).to_excel(writer, sheet_name="Per Produk", index=False)

        pd.DataFrame(
            [
                {"Wilayah": k, "Pendapatan": v}
                for k, v in report.revenue_by_region.items()
            ]
        ).to_excel(writer, sheet_name="Per Wilayah", index=False)

    print(f"\n  Laporan Excel disimpan ke: {destination}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csv-report-cli",
        description="Ubah CSV penjualan menjadi laporan ringkasan di terminal.",
    )
    parser.add_argument("csv_file", type=Path, help="Path ke file CSV penjualan.")
    parser.add_argument(
        "--excel",
        type=Path,
        metavar="OUTPUT.xlsx",
        help="Ekspor juga laporan ke file Excel (butuh pandas + openpyxl).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        transactions = parse_csv(args.csv_file)
    except (FileNotFoundError, CsvFormatError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not transactions:
        print("Tidak ada data valid untuk diproses.", file=sys.stderr)
        return 1

    report = build_report(transactions)
    print_report(report)

    if args.excel:
        args.excel.parent.mkdir(parents=True, exist_ok=True)
        export_excel(report, args.excel)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())