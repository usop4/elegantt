import unittest
import inspect

import elegantt
import elegantt.utils
import elegantt.command

import datetime

from PIL import Image

class TestScenario(unittest.TestCase):

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