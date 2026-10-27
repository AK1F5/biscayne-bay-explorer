from datetime import timedelta
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from bay.data import MEASUREMENTS, load_survey

APP = Path(__file__).resolve().parents[1] / "app.py"


@pytest.fixture
def app():
    return AppTest.from_file(str(APP), default_timeout=20).run()


def test_app_starts_with_two_charts_and_full_dataset(app):
    assert not app.exception
    assert not app.warning
    assert len(app.get("plotly_chart")) == 2
    assert len(app.dataframe[0].value) == 942
    assert "942 of 942 observations" in " ".join(item.value for item in app.markdown)


@pytest.mark.parametrize("measurement", list(MEASUREMENTS))
def test_every_measurement_updates_without_invalid_comparison(app, measurement):
    app.selectbox(key="measurement").select(measurement).run()
    assert not app.exception
    assert app.selectbox(key="comparison").value != measurement
    assert len(app.get("plotly_chart")) == 2


def test_single_sample_is_visible_and_statistics_are_defined(app):
    first = load_survey()["Timestamp"].min().to_pydatetime()
    app.slider(key="time_window").set_value((first, first)).run()
    assert not app.exception
    assert len(app.dataframe[0].value) == 1
    assert any("single reading" in item.value for item in app.markdown)
    assert any("Correlation needs" in item.value for item in app.info)


def test_empty_interval_gives_recovery_guidance(app):
    timestamps = load_survey()["Timestamp"]
    before_gap = timestamps.loc[timestamps.shift(-1) - timestamps > timedelta(seconds=1)].iloc[
        0
    ]
    missing = (before_gap + timedelta(seconds=1)).to_pydatetime()
    app.slider(key="time_window").set_value((missing, missing)).run()
    assert not app.exception
    assert any("No observations" in item.value for item in app.info)
    assert not app.get("plotly_chart")


def test_points_toggle_and_reset_restore_default_controls(app):
    first = load_survey()["Timestamp"].min().to_pydatetime()
    app.selectbox(key="measurement").select("Salinity").run()
    app.slider(key="time_window").set_value((first, first)).run()
    app.checkbox(key="show_points").check().run()
    app.button[0].click().run()
    assert not app.exception
    assert app.selectbox(key="measurement").value == "Dissolved oxygen"
    assert app.selectbox(key="comparison").value == "Temperature"
    assert app.checkbox(key="show_points").value is False
    assert len(app.dataframe[0].value) == 942


def test_clearing_table_columns_preserves_row_and_time(app):
    app.multiselect(key="table_columns").set_value([]).run()
    assert not app.exception
    assert list(app.dataframe[0].value.columns) == ["Source row", "Timestamp"]
