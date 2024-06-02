import sys
import locale
import pandas as pd

sys.path.insert(0, "../..")

import elegantt
import elegantt.utils
import elegantt.command


def test_parse_mermaid():
    s = """
        task a            :done,    des1, 2024-06-15,2024-06-18
        task b            :active,  des2, 2024-06-20, 2d
        task c            :         des3, after des2, 3d
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
    parsed_events = gchart.parse_mermaid(s)
    assert org_events == parsed_events


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
    parsed_events = gchart.parse_markdown(s)
    assert org_events == parsed_events


def test_parse_mermaid_section():
    s = """
        section task a
        task b            :active,  des2, 2024-06-20, 2d
        task c            :         des3, after des2, 3d
    """
    org_events = [
        {"title": "task a", "start": None, "end": None},
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
    gchart = elegantt.EleGantt((720, 320), (255, 255, 255), today="2024-06-18")
    parsed_events = gchart.parse_mermaid(s)
    assert org_events == parsed_events


def test_parse_markdown_section():
    s = """
        |          |          |task a|
        |2024-06-20|2d        |task b|
        |3d        |          |task c|
    """
    org_events = [
        {"title": "task a", "start": None, "end": None},
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
    gchart = elegantt.EleGantt((720, 320), (255, 255, 255), today="2024-06-18")
    parsed_events = gchart.parse_markdown(s)
    assert org_events == parsed_events


def test_analyze_parsed_events():
    s = """
        section task a
        task b            :active,  des2, 2024-06-20, 2d
        task c            :         des3, after des2, 3d
    """
    gchart = elegantt.EleGantt()
    parsed_events = gchart.parse_mermaid(s)
    analyzed_events = {
        "start": pd.Timestamp("2024-06-20"),
        "end": pd.Timestamp("2024-06-26"),
        "size": 3,
    }
    assert analyzed_events == gchart.analyze_events(parsed_events)


def test_detectfont_after_init():
    # before test on ubuntu
    # sudo apt install fonts-noto-cjk
    gchart = elegantt.EleGantt()
    assert gchart.get_font() == "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"


def test_detectfont_after_setfont():
    gchart = elegantt.EleGantt()
    gchart.set_font("test")
    assert gchart.get_font() == "test"


def test_get_today_default():
    gchart = elegantt.EleGantt()
    assert gchart.get_today() == pd.Timestamp.today().normalize()


def test_get_today_assigned():
    gchart = elegantt.EleGantt(today="2024-04-30")
    assert gchart.get_today() == pd.Timestamp("2024-04-30")


def test_set_holidays():
    holidays = ["2024-06-02"]
    gchart = elegantt.EleGantt()
    gchart.set_holidays(holidays)
    assert gchart.holidays == holidays


def test_get_holidays():
    holidays = ["2024-06-02"]
    gchart = elegantt.EleGantt()
    gchart.set_holidays(holidays)
    assert gchart.get_holidays() == holidays


def test_locale():
    # before test on ubuntu
    # sudo apt install language-pack-ja
    locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")
    gchart = elegantt.EleGantt((720, 320), (255, 255, 255))
    assert gchart.get_today() == pd.Timestamp.today().normalize()
