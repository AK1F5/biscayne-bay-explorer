from math import isnan

import pandas as pd
import pytest

from bay.data import MEASUREMENTS, correlation, filter_survey, load_survey, summarize


@pytest.fixture
def survey():
    return load_survey()


def test_course_data_has_expected_shape_and_full_probe_timestamps(survey):
    assert len(survey) == 942
    assert survey["Timestamp"].min() == pd.Timestamp("2022-02-04 16:18:47")
    assert survey["Timestamp"].max() == pd.Timestamp("2022-02-04 16:34:33")
    assert survey["Timestamp"].is_monotonic_increasing
    assert survey["Source row"].nunique() == 942


def test_filter_includes_endpoints_and_can_return_empty(survey):
    start = pd.Timestamp("2022-02-04 16:18:47")
    end = pd.Timestamp("2022-02-04 16:18:49")
    selected = filter_survey(survey, start, end)
    assert selected["Source row"].tolist() == [1, 2, 3]
    assert filter_survey(survey, end, start).empty


def test_oxygen_statistics_match_independent_reference(survey):
    result = summarize(survey, MEASUREMENTS["Dissolved oxygen"])
    assert result["count"] == 942
    assert result["missing"] == 0
    assert result["minimum"] == pytest.approx(5.03)
    assert result["maximum"] == pytest.approx(6.48)
    assert result["mean"] == pytest.approx(5.37463906581741)


def test_summary_excludes_missing_infinite_values_without_clipping():
    frame = pd.DataFrame({"ODO mg/L": [2.0, float("nan"), float("inf"), -1.0, 8.0]})
    result = summarize(frame, MEASUREMENTS["Dissolved oxygen"])
    assert result["count"] == 3
    assert result["missing"] == 2
    assert result["mean"] == 3.0
    assert result["minimum"] == -1.0
    assert result["change"] == 6.0


def test_empty_and_single_observation_summaries_are_defined(survey):
    empty = summarize(survey.iloc[:0], MEASUREMENTS["Dissolved oxygen"])
    single = summarize(survey.iloc[:1], MEASUREMENTS["Dissolved oxygen"])
    assert empty["count"] == 0
    assert isnan(empty["mean"])
    assert empty["change"] is None
    assert single["change"] is None


def test_correlation_handles_constant_and_too_few_pairs(survey):
    x = MEASUREMENTS["Temperature"]
    y = MEASUREMENTS["Dissolved oxygen"]
    constant = survey.iloc[:5].copy()
    constant[x.column] = 1
    assert correlation(constant, x, y) is None
    assert correlation(survey.iloc[:2], x, y) is None
    assert -1 <= correlation(survey, x, y) <= 1


def test_bad_schema_produces_actionable_error(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("Time,Temperature\n12:00,20\n")
    with pytest.raises(ValueError, match="missing required columns"):
        load_survey(path)


def test_invalid_timestamp_is_not_silently_dropped(tmp_path, survey):
    path = tmp_path / "bad-time.csv"
    frame = survey.iloc[:2].drop(columns=["Source row", "Timestamp"]).copy()
    frame.loc[0, "Time hh:mm:ss"] = "invalid"
    frame.to_csv(path, index=False)
    with pytest.raises(ValueError, match="dates or times are invalid"):
        load_survey(path)
