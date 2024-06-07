import sys
import locale
import pandas as pd

sys.path.insert(0, "../..")

import elegantt
import elegantt.utils
import elegantt.command


def t(datestr):
    return pd.Timestamp(datestr)


def test_calc_end_date_1():
    g = elegantt.EleGantt()
    assert g.calc_end_date(t("2024-06-03"), 2) == t("2024-06-04")


def test_calc_end_date_2():
    g = elegantt.EleGantt()
    g.set_holidays(["2024-06-07"])
    assert g.calc_end_date(t("2024-06-03"), 5) == t("2024-06-10")


def test_parse_markdown():
    g = elegantt.EleGantt()
    g.set_holidays(["2024-06-12"])
    s = """
        |2024-06-03|2d        |a   |
        |1d        |          |b   |
        |3d        |          |c   |
        |section   |          |d   |
        |2d        |          |e   |
            """
    org_events = [
        {
            "start": t("2024-06-03"),
            "end": t("2024-06-04"),
            "title": "a",
        },
        {
            "start": t("2024-06-05"),
            "end": t("2024-06-05"),
            "title": "b",
        },
        {
            "start": t("2024-06-06"),
            "end": t("2024-06-10"),
            "title": "c",
        },
        {
            "start": None,
            "end": None,
            "title": "d",
        },
        {
            "start": t("2024-06-11"),
            "end": t("2024-06-13"),
            "title": "e",
        },
    ]
    parsed_events = g.parse_markdown(s)
    assert org_events == parsed_events


def test_parse_mermaid():
    g = elegantt.EleGantt()
    g.set_holidays(["2024-06-12"])
    s = """
        a            :done,    des1, 2024-06-03,2d
        b            :active,  des2, 1d
        c            :         des3, 3d
        section d
        e            :         2d
    """
    org_events = [
        {
            "start": t("2024-06-03"),
            "end": t("2024-06-04"),
            "title": "a",
        },
        {
            "start": t("2024-06-05"),
            "end": t("2024-06-05"),
            "title": "b",
        },
        {
            "start": t("2024-06-06"),
            "end": t("2024-06-10"),
            "title": "c",
        },
        {
            "start": None,
            "end": None,
            "title": "d",
        },
        {
            "start": t("2024-06-11"),
            "end": t("2024-06-13"),
            "title": "e",
        },
    ]
    parsed_events = g.parse_mermaid(s)
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
        "start": t("2024-06-20"),
        "end": t("2024-06-26"),
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
    assert gchart.get_today() == t("2024-04-30")


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
