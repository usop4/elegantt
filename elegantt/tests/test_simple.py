import os
import sys

sys.path.insert(0, "../..")

import elegantt
import elegantt.utils
import elegantt.command

from PIL import Image, ImageChops

import re

import pandas as pd


def t(datestr):
    return pd.Timestamp(datestr)


def test_simple_draw():
    g = elegantt.EleGantt(firstday="2024-06-17")
    g.draw_calendar()
    g.draw_campain("2024-06-17", "2024-06-17", "task a")
    g.draw_campain("2024-06-18", "2024-06-18", "task b")
    imgpath = os.path.dirname(__file__) + "/img/"
    g.save(imgpath + "test_simple_draw.png")


def test_simple_scenario():
    g = elegantt.EleGantt()
    g.set_max_day(21)
    s = """
    task a:2024-06-17,1d
    task b:1d
    task c:1d
    """
    g.auto_draw(s, firstday="2024-06-17")
    imgpath = os.path.dirname(__file__) + "/img/"
    g.save(imgpath + "test_simple_scenario.png")


def test_simple_parse():
    g = elegantt.EleGantt()
    s = """
    task a : 2024-06-17,1d
    task b : 1d
    """
    a = g.parse_mermaid(s)
    b = [
        {"title": "task a", "start": t("2024-06-17"), "end": t("2024-06-17")},
        {"title": "task b", "start": t("2024-06-18"), "end": t("2024-06-18")},
    ]
    assert a == b


def test_diff_image():
    imgpath = os.path.dirname(__file__) + "/img/"
    testpath = os.path.dirname(__file__) + "/"

    image1 = Image.open(imgpath + "test_auto_draw_section.png")
    image2 = Image.open(testpath + "img/test_section.png")
    diff = ImageChops.difference(image1, image2)
    diff.save(imgpath + "diff.png")
