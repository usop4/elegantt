import unittest
import inspect

import sys
sys.path.insert(0, '../..')

import elegantt
import elegantt.utils
import elegantt.command

import datetime
import locale

from PIL import Image
from PIL import ImageChops

class TestSimple(unittest.TestCase):

    def setUp(self):
        gchart = elegantt.EleGantt( (372, 190),(255,255,255),today="2024-05-20",firstday="2024-05-20")
        gchart.set_max_day(11)
        gchart.draw_calendar()
        gchart.draw_campain(None,None,"task a")
        gchart.draw_campain("2024-05-20","2024-05-23","task b")
        gchart.draw_campain("2024-05-24","2024-05-30","task c")
        gchart.save("test_section.png")

    def test_analyze_parsed_events(self,s="""
            section task a
            task b            :active,  des2, 2024-05-20, 4d
            task c            :         des3, after des2, 7d
        """):
        gchart = elegantt.EleGantt()
        parsed_events = gchart.parse_mermaid(s)
        analyzed_events = {
            "start": datetime.datetime.strptime("2024-05-20","%Y-%m-%d"),
            "end": datetime.datetime.strptime("2024-05-30","%Y-%m-%d"),
            "size": 3
        }
        self.assertEqual(analyzed_events,gchart.analyze_events(parsed_events))

    def test_auto_resize(self,s="""
            section task a
            task b            :active,  des2, 2024-05-20, 4d
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

    def test_command_line_mermaid(self):
        elegantt.command.main(args=["sample_mermaid.txt"])
        self.assertEqual(Image.open("test_section.png"),Image.open("sample_mermaid.png"))



