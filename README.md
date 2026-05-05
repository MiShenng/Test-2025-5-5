# UNFCCC COP Research Data

Raw datasets for the UNFCCC / COP discourse-power research project.
Sources fetched on 2026-05-05 

## Layout

```
data/raw/
├── ndc-fulltext/                ← WRI Climate Watch — full text of all NDCs (HTML, ~197 countries)
├── unfccc-ghg-git/              ← openclimatedata — UNFCCC GHG inventory CSVs (Annex I + Non-Annex I)
├── unfccc-attendance/           ← Bagozzi et al. 2024 — individual attendance data 1991–2023 (CSV)
├── enb-mining-castro2025/       ← Castro et al. 2025 — ENB negotiation mining code (data via SwissUbase)
└── climate-watch-historical-emissions.csv.gz   ← Climate Watch historical emissions API dump (1.5M rows)
```

## Sources

| # | Dataset | Origin | Coverage | Size on disk |
|---|---------|--------|----------|--------------|
| 1 | NDC full text (HTML) | [WRI-ClimateWatch/ndc](https://github.com/WRI-ClimateWatch/ndc) | All Parties, all submission rounds | 232 MB |
| 2 | UNFCCC GHG inventory | [openclimatedata/unfccc-detailed-data-by-party](https://github.com/openclimatedata/unfccc-detailed-data-by-party) | Annex I + Non-Annex I, time series | 300 MB |
| 3 | UNFCCC attendance | [bagozzib/UNFCCC-Attendance-Data](https://github.com/bagozzib/UNFCCC-Attendance-Data) | 1991–2023, 310k records, 19 vars | 25 MB (gzipped) |
| 4 | ENB negotiation mining code | [victorkristof/enb-mining](https://github.com/victorkristof/enb-mining) | 1995–2023 ENB summaries | 15 MB |
| 5 | Climate Watch historical emissions | [climatewatchdata.org API](https://www.climatewatchdata.org/api/v1/data/historical_emissions) | All countries, all sectors/gases, 1850–present | 6 MB (gzipped) |

## Notes on compression

Two source files exceed GitHub's 50 MB warning threshold and were gzipped:

- `climate-watch-historical-emissions.csv` (105 MB → 6 MB)
- `unfccc-attendance/master data/cops.cleaned.csv` (71 MB → 10 MB)
- `unfccc-attendance/master data/cops.cleaned.translated.csv` (64 MB → 10 MB)

Decompress before use, e.g.:

```bash
gunzip -k data/raw/climate-watch-historical-emissions.csv.gz
```

Or read directly in Python / R:

```python
import pandas as pd
df = pd.read_csv("data/raw/climate-watch-historical-emissions.csv.gz", compression="gzip")
```

```r
df <- read.csv(gzfile("data/raw/climate-watch-historical-emissions.csv.gz"))
```

## Castro et al. 2025 — note on data access

The negotiation interaction dataset (DOI [10.48573/8VQM-7Z98](https://doi.org/10.48573/8VQM-7Z98))
is hosted on SwissUbase, which requires institutional registration to download.
The associated coding pipeline is included here in `enb-mining-castro2025/`.
Request the dataset directly from SwissUbase if needed.

## Pending sources (not yet fetched)

These are documented in the data plan but were not pulled in this batch:

- COP final decisions corpus (1,034 PDFs from `unfccc.int/decisions`) — requires polite scraping
- Pre-2014 Party submissions archive — requires scraping
- Non-Annex I National Communications and BURs — PDFs per party

## Citation

If you use this compilation, cite the underlying sources directly. Key papers:

- Castro, P., Kristof, V., Kammerer, M., et al. (2025). *Participation, Cooperation and Conflict in UN Climate Negotiations.* **Scientific Data** 12. https://doi.org/10.1038/s41597-025-06262-4
- Bagozzi, B., et al. (2024). *Individual attendance data for over 30 years of international climate change talks.* **Scientific Data** 11, 1134. https://doi.org/10.1038/s41597-024-03978-7
