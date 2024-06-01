import pandas as pd

import sys

sys.path.insert(0, "../..")

import elegantt
import elegantt.utils
import elegantt.command


def test_simple_scenario():
    chartsize = (720, 320)
    bgcolor = (255, 255, 255)
    gchart = elegantt.EleGantt(chartsize, bgcolor, today="2024-06-03")
    gchart.set_max_day(14)
    gchart.draw_calendar()
    gchart.draw_campain("2024-06-03", "2024-06-07", "Task 1 03-07")
    gchart.draw_campain("2024-06-06", "2024-06-10", "Task 2 06-10")
    gchart.draw_campain("2024-06-24", "2024-06-30", "Task 3")
    gchart.save("img/test_simple_scenario.png")


def test_parse_markdown():
    s = """
    |2024-06-15|2024-06-18|task a|
    |2024-06-20|2d        |task b|
    |3d        |          |task c|
"""
    org_events = [
        {
            "title": "task a",
            "start": pd.Timestamp("2024-06-15"),
            "end": pd.Timestamp("2024-06-18"),
        },
        {
            "title": "task b",
            "start": pd.Timestamp("2024-06-20"),
            "end": pd.Timestamp("2024-06-21"),
        },
        {
            "title": "task c",
            "start": pd.Timestamp("2024-06-24"),
            "end": pd.Timestamp("2024-06-26"),
        },
    ]
    gchart = elegantt.EleGantt()
    events = gchart.parse_markdown(s)
    assert events == org_events
