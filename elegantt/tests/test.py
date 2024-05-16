import unittest

import elegantt
import elegantt.utils
import elegantt.command

import datetime
import locale

from PIL import Image
from PIL import ImageChops

class TestFirst(unittest.TestCase):

    def test_library(self):
        gchart = elegantt.EleGantt( (720, 320),(255,255,255),today="2019-10-18")
        gchart.draw_calendar()
        gchart.draw_campain("2019-10-15","2019-10-18","task a")
        gchart.draw_campain("2019-10-20","2019-10-23","task b")
        gchart.draw_campain("2019-10-24","2019-10-30","task c")
        org = Image.open("test_basic_1.png")
        gchart.save("test_basic_1.png")
        dst = Image.open("test_basic_1.png")
        self.assertEqual(org,dst)

    def test_resize(self):
        gchart = elegantt.EleGantt( (720, 320),(255,255,255),today="2019-10-18")
        gchart.resize( (720, 320),(255,255,255))
        gchart.draw_calendar()
        gchart.draw_campain("2019-10-15","2019-10-18","task a")
        gchart.draw_campain("2019-10-20","2019-10-23","task b")
        gchart.draw_campain("2019-10-24","2019-10-30","task c")
        org = Image.open("test_basic_1.png")
        gchart.save("test_basic_1.png")
        dst = Image.open("test_basic_1.png")
        self.assertEqual(org,dst)

    def test_parse_mermaid(self,s="""
            task a            :done,    des1, 2019-10-15,2019-10-18
            task b            :active,  des2, 2019-10-20, 4d
            task c            :         des3, after des2, 7d
        """):
        org_events = [
            {"title":"task a","start":datetime.datetime(2019, 10, 15, 0, 0),"end":datetime.datetime(2019, 10, 18, 0, 0)},
            {"title":"task b","start":datetime.datetime(2019, 10, 20, 0, 0),"end":datetime.datetime(2019, 10, 23, 0, 0)},
            {"title":"task c","start":datetime.datetime(2019, 10, 24, 0, 0),"end":datetime.datetime(2019, 10, 30, 0, 0)}
        ]
        gchart = elegantt.EleGantt( (720, 320),(255,255,255),today="2019-10-18")
        parsed_events = gchart.parse_mermaid(s)
        self.assertEqual(org_events,parsed_events)

    def test_parse_and_draw(self,s="""
            task a            :done,    des1, 2019-10-15,2019-10-18
            task b            :active,  des2, 2019-10-20, 4d
            task c            :         des3, after des2, 7d
        """):
        gchart = elegantt.EleGantt( (720, 320),(255,255,255),today="2019-10-18")
        parsed_events = gchart.parse_mermaid(s)
        gchart.draw_calendar()
        for event in parsed_events:
            start = event["start"].strftime("%Y-%m-%d")
            end   = event["end"].strftime("%Y-%m-%d")
            gchart.draw_campain(start,end,event["title"])
        org = Image.open("test_basic_1.png")
        gchart.save("test_basic_1.png")
        dst = Image.open("test_basic_1.png")
        self.assertEqual(org,dst)

    def test_command_line(self):
        elegantt.command.main(args=["sample.csv"])

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