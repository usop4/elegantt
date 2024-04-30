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
        gchart.draw_campain("2019-10-15","2019-10-18","こんにちは")
        gchart.draw_campain("2019-10-20","2019-10-23","こんにちは")
        gchart.draw_campain("2019-10-24","2019-10-30","こんにちは")
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
        gchart = elegantt.EleGantt( (720, 320),(255,255,255),"2024-04-30")
        self.assertEqual(gchart.get_today(),datetime.date.fromisoformat("2024-04-30"))

    # before test on ubuntu
    # sudo apt install language-pack-ja
    def test_locale(self):

        locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
        gchart = elegantt.EleGantt( (720, 320),(255,255,255))
        self.assertEqual(gchart.get_today(),datetime.date.today())

if __name__ == '__main__':
    unittest.main()