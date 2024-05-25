import unittest
import inspect

import elegantt
import elegantt.utils
import elegantt.command

import datetime
import locale

from PIL import Image
from PIL import ImageChops

class TestMain(unittest.TestCase):

    # この後のテストで作成するファイルを生成
    def setUp(self):
        # 月曜始まり
        gchart = elegantt.EleGantt( (720, 320),(255,255,255),today="2024-06-18")
        gchart.draw_calendar()
        gchart.draw_campain("2024-06-15","2024-06-18","task a")
        gchart.draw_campain("2024-06-20","2024-06-23","task b")
        gchart.draw_campain("2024-06-24","2024-06-30","task c")
        gchart.save("test_basic_monday.png")

        # 開始日を指定
        gchart = elegantt.EleGantt( (720, 320),(255,255,255),today="2024-06-18",firstday="2024-06-15")
        gchart.draw_calendar()
        gchart.draw_campain("2024-06-15","2024-06-18","task a")
        gchart.draw_campain("2024-06-20","2024-06-23","task b")
        gchart.draw_campain("2024-06-24","2024-06-30","task c")
        gchart.save("test_basic_firstday.png")

        gchart = elegantt.EleGantt( (372, 190),(255,255,255),today="2024-06-20",firstday="2024-06-20")
        gchart.set_max_day(11)
        gchart.draw_calendar()
        gchart.draw_campain(None,None,"task a")
        gchart.draw_campain("2024-06-20","2024-06-23","task b")
        gchart.draw_campain("2024-06-24","2024-06-30","task c")
        gchart.save("test_section.png")

    # firstdayを月曜日にして「月曜始まり（引数省略）」と同じになるかを確認
    def test_today_and_firstday_as_monday(self):
        gchart = elegantt.EleGantt( (720, 320),(255,255,255),today="2024-06-18",firstday="2024-06-17")
        gchart.draw_calendar()
        gchart.draw_campain("2024-06-15","2024-06-18","task a")
        gchart.draw_campain("2024-06-20","2024-06-23","task b")
        gchart.draw_campain("2024-06-24","2024-06-30","task c")
        image_name = inspect.currentframe().f_code.co_name + ".png"
        gchart.save(image_name)
        self.assertEqual(Image.open("test_basic_monday.png"),Image.open(image_name))

    def test_resize(self):
        gchart = elegantt.EleGantt( (720, 320),(255,255,255),today="2024-06-18")
        gchart.resize( (720, 320),(255,255,255),today="2024-06-18")
        gchart.draw_calendar()
        gchart.draw_campain("2024-06-15","2024-06-18","task a")
        gchart.draw_campain("2024-06-20","2024-06-23","task b")
        gchart.draw_campain("2024-06-24","2024-06-30","task c")
        image_name = inspect.currentframe().f_code.co_name + ".png"
        gchart.save(image_name)
        self.assertEqual(Image.open("test_basic_monday.png"),Image.open(image_name))

    def test_resize_today_and_firstday(self):
        gchart = elegantt.EleGantt( (720, 320),(255,255,255),today="2024-06-18",firstday="2024-06-15")
        gchart.resize( (720, 320),(255,255,255),today="2024-06-18",firstday="2024-06-15")
        gchart.draw_calendar()
        gchart.draw_campain("2024-06-15","2024-06-18","task a")
        gchart.draw_campain("2024-06-20","2024-06-23","task b")
        gchart.draw_campain("2024-06-24","2024-06-30","task c")
        image_name = inspect.currentframe().f_code.co_name + ".png"
        gchart.save(image_name)
        self.assertEqual(Image.open("test_basic_firstday.png"),Image.open(image_name))

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

    def test_parse_and_draw(self,s="""
            task a            :done,    des1, 2024-06-15,2024-06-18
            task b            :active,  des2, 2024-06-20, 4d
            task c            :         des3, after des2, 7d
        """):
        gchart = elegantt.EleGantt( (720, 320),(255,255,255),today="2024-06-18")
        parsed_events = gchart.parse_mermaid(s)
        gchart.draw_calendar()
        for event in parsed_events:
            start = event["start"].strftime("%Y-%m-%d")
            end   = event["end"].strftime("%Y-%m-%d")
            gchart.draw_campain(start,end,event["title"])
        image_name = inspect.currentframe().f_code.co_name + ".png"
        gchart.save(image_name)
        self.assertEqual(Image.open("test_basic_monday.png"),Image.open(image_name))

    def test_parse_and_draw_section(self,s="""
            section task a
            task b            :active,  des2, 2024-06-20, 4d
            task c            :         des3, after des2, 7d
        """):
        gchart = elegantt.EleGantt( (372, 190),(255,255,255),today="2024-06-20",firstday="2024-06-20")
        gchart.set_max_day(11)
        parsed_events = gchart.parse_mermaid(s)
        gchart.draw_calendar()
        for event in parsed_events:
            start = event["start"].strftime("%Y-%m-%d") if event["start"] else None
            end = event["end"].strftime("%Y-%m-%d") if event["end"] else None
            gchart.draw_campain(start,end,event["title"])
        image_name = inspect.currentframe().f_code.co_name + ".png"
        gchart.save(image_name)
        self.assertEqual(Image.open("test_section.png"),Image.open(image_name))

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

    def test_auto_resize(self,s="""
            section task a
            task b            :active,  des2, 2024-06-20, 4d
            task c            :         des3, after des2, 7d
        """):
        gchart = elegantt.EleGantt()
        parsed_events = gchart.parse_mermaid(s)
        gchart.auto_resize(parsed_events)
        gchart.draw_calendar()
        for event in parsed_events:
            start = event["start"].strftime("%Y-%m-%d") if event["start"] else None
            end = event["end"].strftime("%Y-%m-%d") if event["end"] else None
            gchart.draw_campain(start,end,event["title"])
        image_name = inspect.currentframe().f_code.co_name + ".png"
        gchart.save(image_name)
        self.assertEqual(Image.open("test_section.png"),Image.open(image_name))

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