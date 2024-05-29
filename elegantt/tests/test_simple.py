import sys
sys.path.insert(0, '../..')

import elegantt
import elegantt.utils
import elegantt.command

import datetime
import pprint

def test_parse_markdown():
    s =  """
    |2024-06-15|2024-06-18|task a|
    |2024-06-20|4d        |task b|
    |7d        |          |task c|
"""
    org_events = [
        {"title":"task a","start":datetime.datetime(2024, 6, 15, 0, 0),"end":datetime.datetime(2024, 6, 18, 0, 0)},
        {"title":"task b","start":datetime.datetime(2024, 6, 20, 0, 0),"end":datetime.datetime(2024, 6, 23, 0, 0)},
        {"title":"task c","start":datetime.datetime(2024, 6, 24, 0, 0),"end":datetime.datetime(2024, 6, 30, 0, 0)}
    ]

    gchart = elegantt.EleGantt()
    events =gchart.parse_markdown(s)
    pprint.pprint(events)
    assert events == org_events

