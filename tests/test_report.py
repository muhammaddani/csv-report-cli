"""Test untuk csv-report-cli.

Menguji logika inti: pembacaan CSV, validasi, agregasi, dan format mata uang.
Jalankan dengan:

    pytest -v
"""

import sys
from pathlib import Path

import pytest

# Pastikan folder src bisa diimpor tanpa instalasi paket.
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))

from report import (  # noqa: E402
    CsvFormatError,
    build_report,
    format_currency,
    parse_csv,
    print_report,
)


def write_csv(tmp_path: Path, content: str) -> Path:
    path = tmp_path / "data.csv"
    path.write_text(content, encoding="utf-8")
    return path


HEADER = "date,product,region,quantity,unit_price\n"


class TestParseCsv:
    def test_reads_valid_rows(self, tmp_path):
        path = write_csv(
            tmp_path,
            HEADER + "2026-01-05,Kopi,Jakarta,10,45000\n",
        )
        rows = parse_csv(path)
        assert len(rows) == 1
        assert rows[0].product == "Kopi"
        assert rows[0].revenue == 450000

    def test_missing_file_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            parse_csv(tmp_path / "nope.csv")

    def test_missing_column_raises(self, tmp_path):
        path = write_csv(tmp_path, "date,product,region\n2026-01-05,Kopi,Jakarta\n")
        with pytest.raises(CsvFormatError):
            parse_csv(path)

    def test_bad_row_is_skipped_not_fatal(self, tmp_path):
        path = write_csv(
            tmp_path,
            HEADER
            + "2026-01-05,Kopi,Jakarta,10,45000\n"
            + "2026-01-06,Rusak,Jakarta,abc,45000\n",
        )
        rows = parse_csv(path)
        assert len(rows) == 1

    def test_utf8_bom_is_handled(self, tmp_path):
        path = tmp_path / "bom.csv"
        path.write_text(HEADER + "2026-01-05,Kopi,Jakarta,1,1000\n", encoding="utf-8-sig")
        assert len(parse_csv(path)) == 1


class TestBuildReport:
    def _sample(self, tmp_path):
        path = write_csv(
            tmp_path,
            HEADER
            + "2026-01-05,Kopi,Jakarta,10,45000\n"
            + "2026-01-06,Teh,Bandung,5,25000\n"
            + "2026-01-07,Kopi,Bandung,2,45000\n",
        )
        return build_report(parse_csv(path))

    def test_totals(self, tmp_path):
        report = self._sample(tmp_path)
        assert report.transaction_count == 3
        assert report.total_units == 17
        assert report.total_revenue == 450000 + 125000 + 90000

    def test_revenue_by_product(self, tmp_path):
        report = self._sample(tmp_path)
        assert report.revenue_by_product["Kopi"] == 540000
        assert report.revenue_by_product["Teh"] == 125000

    def test_revenue_by_region(self, tmp_path):
        report = self._sample(tmp_path)
        assert report.revenue_by_region["Jakarta"] == 450000
        assert report.revenue_by_region["Bandung"] == 215000

    def test_best_selling_product(self, tmp_path):
        report = self._sample(tmp_path)
        assert report.best_selling_product == ("Kopi", 12)


class TestFormatting:
    def test_currency_uses_dot_thousands(self):
        assert format_currency(6227000) == "Rp 6.227.000"

    def test_currency_zero(self):
        assert format_currency(0) == "Rp 0"

    def test_print_report_runs(self, tmp_path, capsys):
        path = write_csv(tmp_path, HEADER + "2026-01-05,Kopi,Jakarta,1,1000\n")
        print_report(build_report(parse_csv(path)))
        out = capsys.readouterr().out
        assert "LAPORAN PENJUALAN" in out
        assert "Rp 1.000" in out