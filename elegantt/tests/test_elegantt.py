import unittest
import inspect

import elegantt
import elegantt.utils
import elegantt.command

import datetime
import locale

from PIL import Image
from PIL import ImageChops

class TestElegantt(unittest.TestCase):

    def test_parse_mermaid(self,s="""
            task a            :done,    des1, 2024-06-15,2024-06-18
            task b            :active,  des2, 2024-06-20, 4d
            task c            :         des3, after des2, 7d
        """):
        org_events = [
            {"title":"task a","start":datetime.datetime(2024, 6, 15, 0, 0),"end":datetime.datetime(2024, 6, 18, 0, 0)},
            {"title":"task b","start":datetime.datetime(2024, 6, 20, 0, 0),"end":datetime.datetime(2024, 6, 23, 0, 0)},
            {"title":"task c","start":datetime.datetime(2024, 6, 24, 0, 0),"end":datetime.datetime(2024, 6, 30, 0, 0)}
        ]
        gchart = elegantt.EleGantt( (720, 320),(255,255,255),today="2024-06-18")
        parsed_events = gchart.parse_mermaid(s)
        self.assertEqual(org_events,parsed_events)

    def test_parse_markdown(self,s="""
            |2024-06-15|2024-06-18|task a|
            |2024-06-20|4d        |task b|
            |7d        |          |task c|
        """):
        org_events = [
            {"title":"task a","start":datetime.datetime(2024, 6, 15, 0, 0),"end":datetime.datetime(2024, 6, 18, 0, 0)},
            {"title":"task b","start":datetime.datetime(2024, 6, 20, 0, 0),"end":datetime.datetime(2024, 6, 23, 0, 0)},
            {"title":"task c","start":datetime.datetime(2024, 6, 24, 0, 0),"end":datetime.datetime(2024, 6, 30, 0, 0)}
        ]
        gchart = elegantt.EleGantt( (720, 320),(255,255,255),today="2024-06-18")
        parsed_events = gchart.parse_markdown(s)
        self.assertEqual(org_events,parsed_events)

    def test_parse_mermaid_section(self,s="""
            section task a
            task b            :active,  des2, 2024-06-20, 4d
            task c            :         des3, after des2, 7d
        """):
        org_events = [
            {"title":"task a","start":None,"end":None},
            {"title":"task b","start":datetime.datetime(2024, 6, 20, 0, 0),"end":datetime.datetime(2024, 6, 23, 0, 0)},
            {"title":"task c","start":datetime.datetime(2024, 6, 24, 0, 0),"end":datetime.datetime(2024, 6, 30, 0, 0)}
        ]
        gchart = elegantt.EleGantt( (720, 320),(255,255,255),today="2024-06-18")
        parsed_events = gchart.parse_mermaid(s)
        self.assertEqual(org_events,parsed_events)

    def test_parse_markdown_section(self,s="""
            |          |          |task a|
            |2024-06-20|4d        |task b|
            |7d        |          |task c|
        """):
        org_events = [
            {"title":"task a","start":None,"end":None},
            {"title":"task b","start":datetime.datetime(2024, 6, 20, 0, 0),"end":datetime.datetime(2024, 6, 23, 0, 0)},
            {"title":"task c","start":datetime.datetime(2024, 6, 24, 0, 0),"end":datetime.datetime(2024, 6, 30, 0, 0)}
        ]
        gchart = elegantt.EleGantt( (720, 320),(255,255,255),today="2024-06-18")
        parsed_events = gchart.parse_markdown(s)
        self.assertEqual(org_events,parsed_events)

    def test_analyze_parsed_events(self,s="""
            section task a
            task b            :active,  des2, 2024-06-20, 4d
            task c            :         des3, after des2, 7d
        """):
        gchart = elegantt.EleGantt()
        parsed_events = gchart.parse_mermaid(s)
        analyzed_events = {
            "start": datetime.datetime.strptime("2024-06-20","%Y-%m-%d"),
            "end": datetime.datetime.strptime("2024-06-30","%Y-%m-%d"),
            "size": 3
        }
        self.assertEqual(analyzed_events,gchart.analyze_events(parsed_events))

    def test_command_line(self):
        elegantt.command.main(args=["sample.csv"])

    def test_command_line_mermaid(self):
        elegantt.command.main(args=["sample_mermaid.txt"])
        self.assertEqual(Image.open("test_section.png"),Image.open("sample_mermaid.png"))

    # before test on ubuntu
    # sudo apt install fonts-noto-cjk
    def test_detectfont_after_init(self):
        gchart = elegantt.EleGantt( (720, 320),(255,255,255))
        self.assertEqual(gchart.get_font(),"/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")

    def test_detectfont_after_setfont(self):
        gchart = elegantt.EleGantt( (720, 320),(255,255,255))
        gchart.set_font("test")
        self.assertEqual(gchart.get_font(),"test")

    def test_get_today_default(self):
        gchart = elegantt.EleGantt( (720, 320),(255,255,255))
        self.assertEqual(gchart.get_today(),datetime.date.today())

    def test_get_today_assigned(self):
        gchart = elegantt.EleGantt(today="2024-04-30")
        self.assertEqual(gchart.get_today(),datetime.date.fromisoformat("2024-04-30"))

    # before test on ubuntu
    # sudo apt install language-pack-ja
    def test_locale(self):

        locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
        gchart = elegantt.EleGantt( (720, 320),(255,255,255))
        self.assertEqual(gchart.get_today(),datetime.date.today())




if __name__ == '__main__':
    unittest.main()