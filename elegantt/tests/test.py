import unittest

import elegantt
import elegantt.utils
import elegantt.command

from PIL import Image
from PIL import ImageChops

class TestFirst(unittest.TestCase):

    def test_library(self):
        gchart = elegantt.EleGantt( (720, 320),(255,255,255),today="2019-10-15")
        gchart.draw_calendar()
        gchart.draw_campain("2019-10-15","2019-10-18","こんにちは")
        gchart.draw_campain("2019-10-20","2019-10-23","こんにちは")
        gchart.draw_campain("2019-10-24","2019-10-30","こんにちは")
        gchart.draw_campain("2019-10-28","2019-10-30","こんにちは")
        gchart.draw_campain("2019-10-29","2019-10-30","こんにちは")
        org = Image.open("test_basic_1.png")
        gchart.save("test_basic_1.png")
        dst = Image.open("test_basic_1.png")
        self.assertEqual(org,dst)

    def test_command_line(self):
        elegantt.command.main(args=["sample.csv"])

if __name__ == '__main__':
    unittest.main()