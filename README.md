# U.S. Treasury Yield Curve Monitor

Real-time yield curve analysis — inversion detection & macro signals

🔗 **[Live Dashboard](https://yield-curve-monitor-k4ryyapb8m5jihg5ne43we.streamlit.app/)**

---

## Overview

This project monitors the U.S. Treasury yield curve to detect inversion signals and analyze their relationship with macroeconomic conditions and recession risk.

The 2s10s spread (10Y minus 2Y Treasury yield) is one of the most widely tracked recession leading indicators. This dashboard tracks its historical behavior, flags inversion periods, and quantifies anomalies using a rolling z-score.

---

## Key Features

- **2s10s Spread Tracking** — Real-time spread calculation with inversion detection
- **NBER Recession Overlay** — Visual comparison of inversion periods vs. official recessions
- **Yield Curve Shape Analysis** — Full maturity spectrum (3M–30Y) across different rate environments
- **Z-Score Anomaly Detection** — Statistical identification of historically extreme spread levels

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core analysis |
| FRED API (fredapi) | U.S. Treasury yield data |
| pandas | Data manipulation |
| matplotlib | Visualization |
| Streamlit | Interactive dashboard & deployment |

---
## Project Structure

    yield-curve-monitor/
    ├── analysis/
    │   └── metrics.py        # Core analysis functions
    ├── dashboard/
    │   └── app.py            # Streamlit dashboard
    ├── notebooks/
    │   └── analysis.ipynb    # Exploratory analysis
    ├── requirements.txt
    └── README.md
---

## Key Findings

- The 2s10s spread inverted in **2000, 2006–07, and 2022–23**, each preceding or coinciding with economic stress
- The **2022–23 inversion was the deepest on record** (~-1.0%p), yet no NBER recession has been declared — a contested anomaly in current macro discourse
- The rolling z-score contextualizes each inversion within its recent rate environment, avoiding distortion from structurally different rate regimes

---

## Data Source

[Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/) — Federal Reserve Bank of St. Louis
