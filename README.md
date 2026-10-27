# Biscayne Bay Explorer

An interactive Streamlit app for exploring a short aquatic-robot water-quality
survey from Biscayne Bay. Built for **MC – SDIR | Streamlit Data App**, CIS3590.

## Purpose and features

The app helps students compare measurements, examine changes during the survey,
and inspect the data behind the figures.

- Five selectable measurements: dissolved oxygen, temperature, salinity, pH,
  and water-column depth.
- An inclusive time-range slider updates both Plotly charts, the data table,
  and calculated insights together.
- A time-series chart and a paired-measurement scatter chart, each with a title,
  labeled axes, units, hover values, and a visible legend.
- Optional point markers, a reset button, selectable table columns, and CSV downloads.
- Three sections: **Overview**, **Data display**, and **Insights**.
- Documented data limitations, summary statistics, and descriptive correlation.

## Dataset

The bundled `data/biscayneBay_waterquality.csv` comes from the
[CIS3590 Fall 2026 course repository](https://github.com/studentgreg/3590-Fall2026/blob/main/biscayneBay_waterquality.csv).
It is also linked in Canvas Week 3. No API key, upload, or runtime data download is needed.

The file contains **942 observations and 69 original columns**. Full probe
timestamps cover **February 4, 2022, 16:18:47–16:34:33**; no timezone is supplied.
The app uses `Date m/d/y` and `Time hh:mm:ss`, rather than interpreting the
abbreviated vehicle `Time` column as a complete timestamp.

| Displayed measurement | Source field | Unit |
| --- | --- | --- |
| Dissolved oxygen | `ODO mg/L` | mg/L |
| Temperature | `Temp C` | °C |
| Salinity | `Sal ppt` | ppt |
| pH | `pH` | Unitless |
| Water-column depth | `Total Water Column (m)` | m |

The original CSV is preserved. Only header whitespace and analytical timestamps
are normalized in memory. Measurements are not smoothed, interpolated, clipped,
or converted between units. Missing or non-finite values are excluded from
statistics and paired plots; counts are shown in Insights. All readings,
including repeated values, retain equal weight. Source row numbers let users
trace records back to the original file.

Every supplied turbidity value is negative, so turbidity is excluded from the
chart menu and explained in the app. Calibration information is not supplied.
The robot moved during collection; observed differences can reflect both
location and time. This is historical educational data, not a current water
safety assessment. Correlation is descriptive and does not establish causation.
See [dataset provenance](data/README.md) for additional details.

## User instructions

1. Open the app. The course dataset appears automatically.
2. In the sidebar, choose a **Measurement** and adjust **Survey time**.
   On a phone, tap the arrow in the upper-left corner to open the sidebar.
3. Choose **Compare with** to set the scatter plot's horizontal axis. The selected
   main measurement is on the vertical axis.
4. Hover over charts for exact values. Drag to zoom; double-click to reset a chart.
   **Show individual points** adds markers to the time-series line.
5. Open **Data display** to select columns and download the filtered table.
   The expandable field guide also offers the original CSV.
6. Open **Insights** for ranges, means, medians, endpoint differences,
   correlation, and limitations.
7. Click **Reset filters** to restore the full time range, dissolved oxygen,
   temperature comparison, and line-only display.

If a narrow interval contains no samples, the app explains how to recover.
One-sample intervals show a visible point; an undefined correlation is explained
instead of displaying a misleading number. The table scrolls horizontally on
small screens without widening the page.

## Run locally

Use **Python 3.12**. All direct runtime dependencies are pinned in `requirements.txt`.

```bash
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install and run:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Run these commands from the repository root so Streamlit loads `.streamlit/config.toml`.
Data paths are resolved relative to the source file, not the terminal's current directory.

## Tests and quality checks

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
```

Tests cover source data and timestamps, reference statistics, inclusive and empty
filters, missing values, invalid schemas, chart labels and plotted values, every
measurement selector, single-sample behavior, empty intervals, reset, and table
column selection. Streamlit's `AppTest` executes the actual application.
See [verification evidence](docs/VERIFICATION.md) for browser checks.

## Project structure

```text
app.py                    Streamlit sections and controls
bay/data.py               Schema, timestamp parsing, filters, and calculations
bay/charts.py             Plotly chart construction
bay/ui.py                 Styling and reset behavior
data/                     Original course CSV and provenance
tests/                    Data, chart, and Streamlit interaction tests
docs/AGILE.md             Backlog, acceptance criteria, iterations, retrospective
.streamlit/config.toml    App theme
requirements.txt          Runtime dependencies
requirements-dev.txt      Test and formatting tools
```

## Streamlit Community Cloud deployment

Deploy this repository's `main` branch with **`app.py`** as the entrypoint and
**Python 3.12** in Advanced settings. No secrets or external services are required.
The requirements file and bundled data are in the repository.
Deployment instructions follow the
[official Streamlit guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).

## Agile process and attribution

The work uses a prioritized user-story backlog, acceptance criteria, short
implementation iterations, tests, review, and a retrospective.
[The Agile record](docs/AGILE.md) links requirements to verifiable outcomes.

The design follows the course's Week 3 examples: clear headings, sidebar input,
immediate feedback, tabs, and access to underlying data. The implementation
separates data, charts, and UI instead of copying the course's monolithic example.
Implementation and verification were assisted by OpenAI Codex. No peer review,
student reflection, or instructor approval is claimed by that assistance.
