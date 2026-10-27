"""Run with: python -m streamlit run app.py."""

from datetime import timedelta

import pandas as pd
import streamlit as st

from bay.charts import comparison_chart, time_chart
from bay.data import (
    DATA_PATH,
    MEASUREMENTS,
    SOURCE_URL,
    correlation,
    display_table,
    filter_survey,
    load_survey,
    paired_readings,
    summarize,
)
from bay.ui import apply_styles, reset_controls

st.set_page_config(page_title="Biscayne Bay Explorer", page_icon="🌊", layout="wide")
apply_styles()


# Streamlit reruns this script after widget changes; caching avoids rereading the CSV.
@st.cache_data(show_spinner=False)
def get_survey():
    return load_survey()


def render_controls(survey):
    start = survey["Timestamp"].min().to_pydatetime()
    end = survey["Timestamp"].max().to_pydatetime()

    with st.sidebar:
        st.header("Explore the survey")
        st.caption("Change a control to update the charts, table, and insights.")
        selected = st.selectbox("Measurement", list(MEASUREMENTS), key="measurement")
        metric = MEASUREMENTS[selected]
        st.caption(metric.description)

        # A range slider needs distinct bounds; a single-time survey still remains usable.
        if start < end:
            # Keep the range in session state so reset does not conflict with a default value.
            if "time_window" not in st.session_state:
                st.session_state["time_window"] = (start, end)
            window = st.slider(
                "Survey time",
                min_value=start,
                max_value=end,
                step=timedelta(seconds=1),
                format="HH:mm:ss",
                key="time_window",
                help=(
                    "Both endpoints are included. Times are recorded probe times; "
                    "timezone is unknown."
                ),
            )
        else:
            window = (start, end)
            st.caption("This dataset has one recorded time.")

        alternatives = [label for label in MEASUREMENTS if label != selected]
        # Repair the saved comparison if it now matches the newly selected measurement.
        if st.session_state.get("comparison") not in alternatives:
            st.session_state["comparison"] = alternatives[0]
        compare = st.selectbox("Compare with", alternatives, key="comparison")
        points = st.checkbox("Show individual points", key="show_points")
        st.button("Reset filters", on_click=reset_controls, args=(start, end), width="stretch")
        st.divider()
        st.caption("SOURCE · CIS3590 course dataset")
        st.markdown(f"[View the original CSV]({SOURCE_URL})")
        st.caption("A historical snapshot of Biscayne Bay, collected using an aquatic robot.")

    return metric, MEASUREMENTS[compare], window, points


def render_overview(filtered, metric, compare, show_points):
    st.subheader("Follow a measurement through the survey")
    st.write(
        "Use the sidebar to choose a measurement and time window. Hover for exact values, "
        "drag to zoom, and double-click a chart to restore its view. On a phone, open "
        "the sidebar with the arrow at the top left."
    )
    summary = summarize(filtered, metric)
    if summary["count"] == 0:
        st.info(
            "No numeric readings are available for this measurement in the selected window."
        )
        return

    st.plotly_chart(
        time_chart(filtered, metric, show_points),
        use_container_width=True,
        config={"displaylogo": False, "scrollZoom": False},
        key="time_chart",
    )
    st.caption(
        "Each point is one recorded observation; the line connects samples without smoothing. "
        "The vertical scale adapts to the measurement and may not start at zero."
    )
    st.divider()
    st.subheader(f"Compare {metric.label.lower()} and {compare.label.lower()}")
    st.write(
        "Each dot pairs two measurements from the same CSV row. Patterns describe this "
        "survey interval; they do not establish cause and effect."
    )
    pairs = paired_readings(filtered, compare, metric)
    if pairs.empty:
        st.info("No complete pairs are available in this interval.")
    else:
        st.plotly_chart(
            comparison_chart(filtered, compare, metric),
            use_container_width=True,
            config={"displaylogo": False, "scrollZoom": False},
            key="comparison_chart",
        )


def render_data(filtered):
    st.subheader("Inspect the readings")
    st.write("The table uses the charts' time window. Select columns to inspect or export.")
    chosen = st.multiselect(
        "Measurements to display",
        list(MEASUREMENTS),
        default=list(MEASUREMENTS),
        key="table_columns",
    )
    table = display_table(filtered, [MEASUREMENTS[name].column for name in chosen])
    if not chosen:
        st.info(
            "Time and source rows are still shown. Choose a measurement to add its readings."
        )
    st.dataframe(table, hide_index=True, width="stretch", height=400)
    st.caption("Source row is the original data-row number, excluding the CSV header.")
    # Export the displayed table so the download respects both time and column selections.
    st.download_button(
        "Download this table (CSV)",
        table.to_csv(index=False).encode("utf-8"),
        file_name="biscayne_bay_filtered.csv",
        mime="text/csv",
        key="filtered_download",
    )
    with st.expander("Original data and field definitions"):
        st.write(
            "The original CSV includes 69 water-quality and vehicle-telemetry fields. "
            "The download preserves all fields; the explorer charts five measurements."
        )
        st.dataframe(
            pd.DataFrame(
                [
                    {"Measurement": item.axis_label, "CSV field": item.column}
                    for item in MEASUREMENTS.values()
                ]
            ),
            hide_index=True,
            width="stretch",
        )
        st.download_button(
            "Download original course CSV",
            DATA_PATH.read_bytes(),
            file_name=DATA_PATH.name,
            mime="text/csv",
        )


def render_insights(filtered, metric, compare):
    st.subheader("What this interval shows")
    summary = summarize(filtered, metric)
    unit = f" {metric.unit}" if metric.unit else ""
    if not summary["count"]:
        st.info("Choose a window with numeric readings to calculate insights.")
        return

    st.markdown(
        f"Across **{summary['count']:,} readings**, {metric.label.lower()} ranges from "
        f"**{summary['minimum']:.3f}{unit}** to **{summary['maximum']:.3f}{unit}**. "
        f"The mean is **{summary['mean']:.3f}{unit}** and the median is "
        f"**{summary['median']:.3f}{unit}**."
    )
    if summary["change"] is not None:
        st.write(
            f"The last valid reading minus the first is {summary['change']:+.3f}{unit}. "
            "This endpoint difference is not a fitted trend or a long-term change."
        )
    else:
        st.write("A single reading is selected, so an endpoint change cannot be calculated.")

    # The helper returns None for too few pairs or a measurement with no variation.
    coefficient = correlation(filtered, compare, metric)
    if coefficient is None:
        st.info("Correlation needs three paired readings with variation in both measurements.")
    else:
        st.write(
            f"Pearson correlation between {compare.label.lower()} and {metric.label.lower()}: "
            f"r = {coefficient:.3f}, "
            f"using {len(paired_readings(filtered, compare, metric)):,} pairs. "
            "Nearby samples are related in time and space, so this is descriptive rather than "
            "a test of statistical significance."
        )

    st.subheader("Summary for every measurement")
    rows = []
    for item in MEASUREMENTS.values():
        stats = summarize(filtered, item)
        rows.append(
            {
                "Measurement": item.axis_label,
                "Readings": stats["count"],
                "Mean": stats["mean"],
                "Median": stats["median"],
                "Min": stats["minimum"],
                "Max": stats["maximum"],
                "Missing / non-finite": stats["missing"],
            }
        )
    st.dataframe(pd.DataFrame(rows).round(3), hide_index=True, width="stretch")
    st.subheader("Read these results in context")
    st.write(
        "This is a short historical survey along a moving robot's route. Changes may reflect "
        "location as well as time. The file does not document sensor calibration. "
        "It cannot establish current conditions or water safety."
    )
    st.write(
        "All supplied turbidity readings are negative. They remain in the original download, "
        "but are excluded from the chart menu because the file gives no calibration context "
        "for interpreting them."
    )


def main():
    st.markdown(
        '<div class="survey-eyebrow">FIELD NOTES / BISCAYNE BAY</div>', unsafe_allow_html=True
    )
    st.title("A closer look at the bay")
    st.write(
        "Explore water-quality readings from a Biscayne Bay aquatic-robot survey. "
        "Choose a measurement, narrow the time window, and see how the observations relate."
    )
    try:
        survey = get_survey()
    except (OSError, ValueError, pd.errors.ParserError) as error:
        st.error(f"The course dataset could not be loaded. {error}")
        st.info("Restore data/biscayneBay_waterquality.csv from the repository, then reload.")
        st.stop()

    metric, compare, window, show_points = render_controls(survey)
    # Share one filtered dataset across all sections to keep their results consistent.
    filtered = filter_survey(survey, *window)
    survey_date = survey["Timestamp"].min().strftime("%B %d, %Y")
    st.markdown(
        '<div class="survey-context">'
        f"{survey_date} &nbsp; · &nbsp; {len(filtered):,} of {len(survey):,} observations"
        f" &nbsp; · &nbsp; {window[0]:%H:%M:%S}–{window[1]:%H:%M:%S}"
        "</div>",
        unsafe_allow_html=True,
    )
    st.caption("Recorded probe time · timezone not supplied · historical data")

    if filtered.empty:
        st.info(
            "No observations fall in this window. Widen the time range or choose Reset filters."
        )
        # End this rerun before building charts; the sidebar stays available for recovery.
        st.stop()

    overview, data, insights = st.tabs(["Overview", "Data display", "Insights"])
    with overview:
        render_overview(filtered, metric, compare, show_points)
    with data:
        render_data(filtered)
    with insights:
        render_insights(filtered, metric, compare)

    with st.expander("About the data and calculations"):
        st.markdown(f"**Source:** [CIS3590 Fall 2026 course CSV]({SOURCE_URL}).")
        st.write(
            "Probe date and time are parsed as month/day/year and HH:MM:SS, then sorted "
            "chronologically. Both time-filter endpoints are included. Each source row is "
            "one observation; repeated readings are retained. No smoothing, interpolation, "
            "unit conversion, or clipping is applied. Missing and infinite measurements "
            "are omitted from statistics and paired plots, with counts shown in Insights. "
            "Line charts leave gaps for missing numeric readings."
        )
        st.write(
            "Temperature uses Temp C, salinity uses Sal ppt, and oxygen uses ODO mg/L. "
            "Other similarly named sensor fields are not merged. Means and medians are "
            "computed from the selected observations, not weighted by elapsed time."
        )
    st.caption("Biscayne Bay Explorer · MC–SDIR Streamlit Data App · CIS3590")


if __name__ == "__main__":
    main()
