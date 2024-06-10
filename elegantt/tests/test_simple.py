import pandas as pd
import os
import sys

sys.path.insert(0, "../..")

import elegantt
import elegantt.utils
import elegantt.command

from PIL import Image, ImageChops


def test_simple_scenario():
    imgpath = os.path.dirname(__file__) + "/img/"
    gchart = elegantt.EleGantt(today="2024-06-20", firstday="2024-06-20")
    gchart.set_holidays(["2024-06-25"])
    gchart.draw_calendar()
    gchart.draw_campain(None, None, "task a")
    gchart.draw_campain("2024-06-20", "2024-06-21", "task b")
    gchart.draw_campain("2024-06-24", "2024-06-26", "task c")
    gchart.save(imgpath + "test.png")


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


def test_diff_image():
    imgpath = os.path.dirname(__file__) + "/img/"
    testpath = os.path.dirname(__file__) + "/"

    image1 = Image.open(imgpath + "test_basic_monday.png")
    image2 = Image.open(testpath + "img/test_parse_and_draw_from_markdown.png")
    diff = ImageChops.difference(image1, image2)
    diff.save(imgpath + "diff.png")
