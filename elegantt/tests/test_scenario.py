import unittest
import inspect
import os
import sys

sys.path.insert(0, "../..")

import elegantt
import elegantt.utils
import elegantt.command

from PIL import Image


class TestScenario(unittest.TestCase):

    imgpath = ""
    testpath = ""

    # この後のテストで作成するファイルを生成
    def setUp(self):

        self.testpath = os.path.dirname(__file__) + "/"
        self.imgpath = os.path.dirname(__file__) + "/img/"

        # 月曜始まり
        gchart = elegantt.EleGantt(today="2024-06-18")
        gchart.draw_calendar()
        gchart.draw_campain("2024-06-15", "2024-06-18", "task a")
        gchart.draw_campain("2024-06-20", "2024-06-21", "task b")
        gchart.draw_campain("2024-06-24", "2024-06-26", "task c")
        gchart.save(self.imgpath + "test_basic_monday.png")

        # 開始日を指定
        gchart = elegantt.EleGantt(today="2024-06-18", firstday="2024-06-15")
        gchart.draw_calendar()
        gchart.draw_campain("2024-06-15", "2024-06-18", "task a")
        gchart.draw_campain("2024-06-20", "2024-06-21", "task b")
        gchart.draw_campain("2024-06-24", "2024-06-26", "task c")
        gchart.save(self.imgpath + "test_basic_firstday.png")

        gchart = elegantt.EleGantt(today="2024-06-20", firstday="2024-06-20")
        gchart.set_holidays(["2024-06-25"])
        gchart.draw_calendar()
        gchart.draw_campain(None, None, "task a")
        gchart.draw_campain("2024-06-20", "2024-06-21", "task b")
        gchart.draw_campain("2024-06-24", "2024-06-26", "task c")
        gchart.save(self.imgpath + "test_section.png")

    # firstdayを月曜日にして「月曜始まり（引数省略）」と同じになるかを確認
    def test_today_and_firstday_as_monday(self):
        gchart = elegantt.EleGantt(today="2024-06-18", firstday="2024-06-17")
        gchart.draw_calendar()
        gchart.draw_campain("2024-06-15", "2024-06-18", "task a")
        gchart.draw_campain("2024-06-20", "2024-06-21", "task b")
        gchart.draw_campain("2024-06-24", "2024-06-26", "task c")
        image_name = self.imgpath + inspect.currentframe().f_code.co_name + ".png"
        gchart.save(image_name)
        self.assertEqual(
            Image.open(self.imgpath + "test_basic_monday.png"), Image.open(image_name)
        )

    def test_resize(self):
        gchart = elegantt.EleGantt(today="2024-06-18")
        gchart.resize((468, 295), (255, 255, 255), today="2024-06-18")
        gchart.draw_calendar()
        gchart.draw_campain("2024-06-15", "2024-06-18", "task a")
        gchart.draw_campain("2024-06-20", "2024-06-21", "task b")
        gchart.draw_campain("2024-06-24", "2024-06-26", "task c")
        image_name = self.imgpath + inspect.currentframe().f_code.co_name + ".png"
        gchart.save(image_name)
        self.assertEqual(
            Image.open(self.imgpath + "test_basic_monday.png"), Image.open(image_name)
        )

    def test_resize_today_and_firstday(self):
        gchart = elegantt.EleGantt(today="2024-06-18", firstday="2024-06-15")
        gchart.resize(
            (468, 295), (255, 255, 255), today="2024-06-18", firstday="2024-06-15"
        )
        gchart.draw_calendar()
        gchart.draw_campain("2024-06-15", "2024-06-18", "task a")
        gchart.draw_campain("2024-06-20", "2024-06-21", "task b")
        gchart.draw_campain("2024-06-24", "2024-06-26", "task c")
        image_name = self.imgpath + inspect.currentframe().f_code.co_name + ".png"
        gchart.save(image_name)
        self.assertEqual(
            Image.open(self.imgpath + "test_basic_firstday.png"), Image.open(image_name)
        )

    def test_parse_and_draw_from_mermaid(self):
        s = """
            task a            :done, des1, 2024-06-15, 2024-06-18
            task b            :active, des2, 2024-06-20, 2d
            task c            :         des3, after des2, 3d
        """
        gchart = elegantt.EleGantt(today="2024-06-18")
        gchart.auto_draw(s, mode="mermaid")
        image_name = self.imgpath + inspect.currentframe().f_code.co_name + ".png"
        gchart.save(image_name)
        self.assertEqual(
            Image.open(self.imgpath + "test_basic_firstday.png"), Image.open(image_name)
        )

    def test_parse_and_draw_from_markdown(self):
        s = """
        |2024-06-15|2024-06-18|task a|
        |2024-06-20|2d        |task b|
        |3d        |          |task c|
        """
        gchart = elegantt.EleGantt(today="2024-06-18")
        gchart.auto_draw(s, mode="markdown")
        image_name = self.imgpath + inspect.currentframe().f_code.co_name + ".png"
        gchart.save(image_name)
        self.assertEqual(
            Image.open(self.imgpath + "test_basic_firstday.png"), Image.open(image_name)
        )

    def test_auto_draw_section(self):
        s = """
            section task a
            task b            :active, des2, 2024-06-20, 2d
            task c            :         des3, after des2, 2d
        """
        gchart = elegantt.EleGantt(today="2024-06-20", firstday="2024-06-20")
        gchart.set_holidays(["2024-06-25"])
        gchart.set_max_day(14)
        gchart.auto_draw(s, mode="mermaid")
        image_name = self.imgpath + inspect.currentframe().f_code.co_name + ".png"
        gchart.save(image_name)
        self.assertEqual(
            Image.open(self.imgpath + "test_section.png"), Image.open(image_name)
        )

    def test_auto_draw(self):
        s = """
            section task a
            task b            :active, des2, 2024-06-20, 2d
            task c            :         des3, after des2, 2d
        """
        gchart = elegantt.EleGantt()
        gchart.set_holidays(["2024-06-25"])
        gchart.auto_draw(s, mode="mermaid")
        image_name = self.imgpath + inspect.currentframe().f_code.co_name + ".png"
        gchart.save(image_name)
        self.assertEqual(
            Image.open(self.imgpath + "test_section.png"), Image.open(image_name)
        )

    # holidayを設定して、考慮できるかテスト
    def test_holiday(self):
        s = """
            section task a
            task b            :active, des2, 2024-06-20, 2d
            task c            :         des3, after des2, 2d
        """
        gchart = elegantt.EleGantt()
        gchart.set_holidays(["2024-06-25"])
        gchart.auto_draw(s, mode="mermaid")
        image_name = self.imgpath + inspect.currentframe().f_code.co_name + ".png"
        gchart.save(image_name)
        self.assertEqual(
            Image.open(self.imgpath + "test_section.png"), Image.open(image_name)
        )

    def test_command_line(self):
        elegantt.command.main(args=[self.testpath + "sample.csv"])

    def test_command_line_mermaid(self):
        elegantt.command.main(args=[self.testpath + "sample_mermaid.txt"])
        self.assertEqual(
            Image.open(self.imgpath + "test_basic_firstday.png"),
            Image.open(self.testpath + "sample_mermaid.png"),
        )

    def test_command_line_markdown(self):
        elegantt.command.main(args=[self.testpath + "sample_markdown.md"])
        self.assertEqual(
            Image.open(self.imgpath + "test_basic_firstday.png"),
            Image.open(self.testpath + "sample_markdown.png"),
        )
