# How to resume the COP-decision fetch

The fetch script (`scripts/fetch_cop_decisions.py`) is **idempotent**:
files already on disk are skipped, so you can re-run it to pick up where
a previous session left off.

## Quick resume (next session)

```bash
cd /Users/mishenng/Desktop/power/unfccc-data
.venv/bin/python scripts/fetch_cop_decisions.py
```

That's it. Files already in `data/raw/cop_decisions/` are skipped; the
script tries every remaining symbol candidate (1995–2024) and only
downloads the missing ones.

## If `.venv` was deleted

```bash
cd /Users/mishenng/Desktop/power/unfccc-data
python3 -m venv .venv
.venv/bin/pip install cloudscraper requests beautifulsoup4
.venv/bin/python scripts/fetch_cop_decisions.py
```

## Pull the latest checkpoint from GitHub before resuming

If you're on a different machine or pulling a fresh clone:

```bash
git clone https://github.com/MiShenng/Test-2025-5-5.git unfccc-data
cd unfccc-data
python3 -m venv .venv
.venv/bin/pip install cloudscraper requests beautifulsoup4
.venv/bin/python scripts/fetch_cop_decisions.py
```

## After the run completes

The script writes a fetch log to:

```
data/raw/cop_decisions/_fetch_log.csv
```

Inspect it for any non-200 / non-PDF responses. To commit the new files:

```bash
git add data/raw/cop_decisions/
git commit -m "Add additional COP decision PDFs (resumed fetch)"
git push
```

## How long it takes

- Cold run (nothing on disk): roughly **35–45 minutes** for 1995–2024.
  Each candidate symbol takes ~1.5 s with cloudscraper challenge + 0.4 s
  polite delay.
- Warm run (resume): proportional to how many symbols are still missing.
- Each year has ~50 candidate symbols; most return 404 (only ~3–8 PDFs
  per year actually exist).

## What's intentionally **not** automated

The data plan also lists:

- 1,034 individual COP decisions on `unfccc.int/decisions`
- pre-2014 party submissions archive
- Non-Annex I National Communications + Biennial Update Reports

All of these live on `unfccc.int`, which is shielded by Imperva and
blocks scrapers (including cloudscraper). The decision **collections**
we fetch from UN ODS contain the same official text. If you really need
the rest, options are:

1. Headless browser with Playwright/Selenium (slow, brittle).
2. Manual export from the UNFCCC website.
3. Email UNFCCC to request a bulk archive.
