"""Load the course survey without changing the original measurements."""

from dataclasses import dataclass
from math import isfinite
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "biscayneBay_waterquality.csv"
SOURCE_URL = (
    "https://github.com/studentgreg/3590-Fall2026/blob/main/biscayneBay_waterquality.csv"
)


@dataclass(frozen=True)
class Measurement:
    column: str
    label: str
    unit: str
    description: str

    @property
    def axis_label(self) -> str:
        return f"{self.label} ({self.unit})" if self.unit else self.label


MEASUREMENTS = {
    "Dissolved oxygen": Measurement(
        "ODO mg/L",
        "Dissolved oxygen",
        "mg/L",
        "Oxygen dissolved in the water, as measured by the probe.",
    ),
    "Temperature": Measurement(
        "Temp C", "Temperature", "°C", "Water temperature from the probe's Temp C field."
    ),
    "Salinity": Measurement(
        "Sal ppt", "Salinity", "ppt", "Salt concentration in parts per thousand."
    ),
    "pH": Measurement(
        "pH", "pH", "", "The probe's measure of acidity and alkalinity; pH is unitless."
    ),
    "Water-column depth": Measurement(
        "Total Water Column (m)",
        "Water-column depth",
        "m",
        "Total water-column depth reported by the vehicle, in meters.",
    ),
}


def load_survey(path: Path = DATA_PATH) -> pd.DataFrame:
    """Parse full probe timestamps and sort stably; retain the original source row."""
    frame = pd.read_csv(path)
    frame.columns = frame.columns.str.strip()
    required = {"Date m/d/y", "Time hh:mm:ss"}
    required.update(metric.column for metric in MEASUREMENTS.values())
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError(f"The survey is missing required columns: {', '.join(missing)}.")
    if frame.empty:
        raise ValueError("The survey CSV contains no observations.")

    frame.insert(0, "Source row", range(1, len(frame) + 1))
    timestamp_text = frame["Date m/d/y"].astype(str) + " " + frame["Time hh:mm:ss"].astype(str)
    frame.insert(
        1,
        "Timestamp",
        pd.to_datetime(timestamp_text, format="%m/%d/%y %H:%M:%S", errors="coerce"),
    )
    if frame["Timestamp"].isna().any():
        raise ValueError("Some probe dates or times are invalid; check the source CSV.")

    for metric in MEASUREMENTS.values():
        frame[metric.column] = pd.to_numeric(frame[metric.column], errors="coerce")

    return frame.sort_values(["Timestamp", "Source row"], kind="stable").reset_index(drop=True)


def filter_survey(frame: pd.DataFrame, start, end) -> pd.DataFrame:
    """Select both interval endpoints, preserving chronological order."""
    return frame.loc[frame["Timestamp"].between(start, end, inclusive="both")].copy()


def numeric_values(frame: pd.DataFrame, metric: Measurement) -> pd.Series:
    """Exclude only missing and non-finite values; never silently clip readings."""
    values = pd.to_numeric(frame[metric.column], errors="coerce")
    return values.where(values.map(isfinite))


def summarize(frame: pd.DataFrame, metric: Measurement) -> dict:
    values = numeric_values(frame, metric).dropna()
    return {
        "count": len(values),
        "missing": len(frame) - len(values),
        "mean": values.mean(),
        "median": values.median(),
        "minimum": values.min(),
        "maximum": values.max(),
        "change": values.iloc[-1] - values.iloc[0] if len(values) > 1 else None,
    }


def paired_readings(frame: pd.DataFrame, x: Measurement, y: Measurement) -> pd.DataFrame:
    pairs = frame[["Timestamp", "Source row"]].copy()
    pairs[x.column] = numeric_values(frame, x)
    pairs[y.column] = numeric_values(frame, y)
    return pairs.dropna(subset=[x.column, y.column])


def correlation(frame: pd.DataFrame, x: Measurement, y: Measurement) -> float | None:
    pairs = paired_readings(frame, x, y)
    if len(pairs) < 3 or pairs[x.column].nunique() < 2 or pairs[y.column].nunique() < 2:
        return None
    result = pairs[x.column].corr(pairs[y.column])
    return float(result) if isfinite(result) else None


def display_table(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    names = {metric.column: metric.axis_label for metric in MEASUREMENTS.values()}
    return frame[["Source row", "Timestamp", *columns]].rename(columns=names)
