"""Plotly figures with explicit units and visible series legends."""

import pandas as pd
import plotly.graph_objects as go

from bay.data import Measurement, numeric_values, paired_readings

INK = "#183B3D"
TEAL = "#087F8C"
OCHRE = "#A65F16"
PAPER = "#FAFBF7"


def style_chart(figure: go.Figure, title: str, x_label: str, y_label: str) -> go.Figure:
    figure.update_layout(
        title={"text": title, "font": {"size": 17}, "x": 0, "xanchor": "left"},
        xaxis_title=x_label,
        yaxis_title=y_label,
        font={"family": "Source Sans 3, sans-serif", "size": 13, "color": INK},
        paper_bgcolor=PAPER,
        plot_bgcolor=PAPER,
        height=400,
        margin={"l": 8, "r": 12, "t": 90, "b": 32},
        legend={"orientation": "h", "y": 1.13, "x": 0, "title": {"text": ""}},
        showlegend=True,
        hoverlabel={"font_size": 14},
    )
    figure.update_xaxes(showgrid=False, automargin=True, zeroline=False, nticks=5)
    figure.update_yaxes(gridcolor="#DBE5E1", automargin=True, zeroline=False, nticks=5)
    return figure


def time_chart(frame: pd.DataFrame, metric: Measurement, show_points: bool) -> go.Figure:
    figure = go.Figure(
        go.Scatter(
            x=frame["Timestamp"],
            y=numeric_values(frame, metric),
            mode="lines+markers" if show_points or len(frame) == 1 else "lines",
            name="Probe readings"
            if metric.label != "Water-column depth"
            else "Vehicle readings",
            line={"color": TEAL, "width": 2},
            marker={"size": 4},
            connectgaps=False,
            hovertemplate=(
                "%{x|%H:%M:%S}<br>"
                + metric.label
                + ": %{y:.3f} "
                + metric.unit
                + "<extra></extra>"
            ),
        )
    )
    style_chart(figure, f"{metric.label} over time", "Probe time (HH:MM:SS)", metric.axis_label)
    figure.update_xaxes(tickformat="%H:%M:%S")
    return figure


def comparison_chart(frame: pd.DataFrame, x: Measurement, y: Measurement) -> go.Figure:
    pairs = paired_readings(frame, x, y)
    figure = go.Figure(
        go.Scatter(
            x=pairs[x.column],
            y=pairs[y.column],
            mode="markers",
            name="Paired readings",
            customdata=pairs["Timestamp"].dt.strftime("%H:%M:%S"),
            marker={"color": OCHRE, "size": 6, "opacity": 0.65},
            hovertemplate=(
                "%{customdata}<br>"
                + x.axis_label
                + ": %{x:.3f}<br>"
                + y.axis_label
                + ": %{y:.3f}<extra></extra>"
            ),
        )
    )
    return style_chart(figure, "Measurement comparison", x.axis_label, y.axis_label)
