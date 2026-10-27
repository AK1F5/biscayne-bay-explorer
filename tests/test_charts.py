from bay.charts import comparison_chart, time_chart
from bay.data import MEASUREMENTS, load_survey


def test_line_chart_preserves_data_units_title_and_legend():
    survey = load_survey().iloc[:3]
    metric = MEASUREMENTS["Dissolved oxygen"]
    chart = time_chart(survey, metric, False)
    assert list(chart.data[0].y) == [6.48, 6.39, 6.45]
    assert chart.layout.yaxis.title.text == "Dissolved oxygen (mg/L)"
    assert chart.layout.xaxis.title.text == "Probe time (HH:MM:SS)"
    assert chart.layout.title.text == "Dissolved oxygen over time"
    assert chart.layout.showlegend is True
    assert chart.data[0].connectgaps is False


def test_single_point_and_comparison_remain_interpretable():
    survey = load_survey().iloc[:1]
    oxygen = MEASUREMENTS["Dissolved oxygen"]
    temperature = MEASUREMENTS["Temperature"]
    assert time_chart(survey, oxygen, False).data[0].mode == "lines+markers"
    chart = comparison_chart(survey, temperature, oxygen)
    assert list(chart.data[0].x) == [22.56]
    assert list(chart.data[0].y) == [6.48]
    assert chart.layout.xaxis.title.text == "Temperature (°C)"
    assert chart.data[0].name == "Paired readings"
