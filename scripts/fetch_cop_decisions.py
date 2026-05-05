"""
Fetch COP / CMP / CMA decision PDFs from UN ODS (daccess-ods.un.org).

UNFCCC.int is shielded by Imperva and cannot be scraped directly. UN ODS
serves the same official documents by symbol with no anti-bot protection.

Each decision-cycle (COP/CMP/CMA) for years 1995-2024 is enumerated by trying
plausible Add.N suffixes; symbols that 404 are skipped. Real PDFs (~30-100
files total) are saved under data/raw/cop_decisions/.
"""

from __future__ import annotations

import csv
import time
from pathlib import Path

import cloudscraper

OUT_DIR = Path("data/raw/cop_decisions")
OUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH = OUT_DIR / "_fetch_log.csv"

BASE = "https://daccess-ods.un.org/access.nsf/Get?OpenAgent&DS={sym}&Lang=E"

# Year -> COP number map (COP 1 = 1995). CMP started COP 11 (2005). CMA started COP 21 (2015).
COP_YEARS = list(range(1995, 2025))


def candidate_symbols(year: int) -> list[str]:
    """Document symbols to try for one COP year."""
    syms: list[str] = []
    cop_num = year - 1994  # COP 1 was 1995

    # COP decisions: FCCC/CP/<year>/<doc_no>/Add.<N> — the "doc_no" varies; in
    # practice the final-decisions volumes are usually 7, 10, 11, or 12 with
    # Add.1..Add.5. We try a broad grid and keep whatever exists.
    for doc_no in (5, 6, 7, 8, 9, 10, 11, 12, 13, 17):
        for add in range(1, 6):
            syms.append(f"FCCC/CP/{year}/{doc_no}/Add.{add}")

    # CMP decisions (Kyoto): from 2005 onwards
    if year >= 2005:
        for doc_no in (8, 9, 10, 11):
            for add in range(1, 4):
                syms.append(f"FCCC/KP/CMP/{year}/{doc_no}/Add.{add}")

    # CMA decisions (Paris): from 2016 onwards (CMA 1 was Marrakech 2016)
    if year >= 2016:
        for doc_no in (10, 11, 12, 13, 16, 17):
            for add in range(1, 5):
                syms.append(f"FCCC/PA/CMA/{year}/{doc_no}/Add.{add}")

    return syms


def is_pdf(content: bytes, headers: dict) -> bool:
    return content[:5] == b"%PDF-" or headers.get("Content-Type", "").startswith("application/pdf")


def safe_filename(symbol: str) -> str:
    return symbol.replace("/", "_") + ".pdf"


def main() -> None:
    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "darwin", "desktop": True}
    )

    rows: list[dict] = []
    saved = 0
    skipped = 0

    for year in COP_YEARS:
        symbols = candidate_symbols(year)
        for sym in symbols:
            fname = safe_filename(sym)
            target = OUT_DIR / fname
            if target.exists() and target.stat().st_size > 1024:
                # already fetched in a prior run — skip
                rows.append({"year": year, "symbol": sym, "status": "SKIP", "size": target.stat().st_size, "note": "already on disk"})
                saved += 1
                continue

            url = BASE.format(sym=sym)
            try:
                r = scraper.get(url, timeout=45, allow_redirects=True)
            except Exception as exc:
                rows.append({"year": year, "symbol": sym, "status": "ERR", "size": 0, "note": str(exc)[:80]})
                continue

            size = len(r.content)
            if r.status_code == 200 and is_pdf(r.content, r.headers):
                target.write_bytes(r.content)
                rows.append({"year": year, "symbol": sym, "status": "OK", "size": size, "note": fname})
                saved += 1
                print(f"  [{saved:>3}] {sym:<32} -> {fname} ({size/1024:.0f} KB)")
            else:
                skipped += 1
                rows.append(
                    {"year": year, "symbol": sym, "status": str(r.status_code), "size": size, "note": ""}
                )

            time.sleep(0.4)  # polite delay

    with LOG_PATH.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["year", "symbol", "status", "size", "note"])
        w.writeheader()
        w.writerows(rows)

    print()
    print(f"Saved {saved} PDFs, skipped {skipped} non-existent symbols")
    print(f"Log: {LOG_PATH}")


if __name__ == "__main__":
    main()
