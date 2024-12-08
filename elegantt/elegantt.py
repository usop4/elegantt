#!python3
# -*- coding: utf-8 -*-

import json
import re
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

import elegantt.utils


def t(datestr):
    return pd.Timestamp(datestr)


class EleGantt:

    num = 0
    top_margin = 10
    bottom_margin = 10
    left_margin = 10
    cell_width = 32
    date_position = 20
    week_position = 40
    box_position = 60
    box_margin = 5
    box_height = 40
    font_size = 12

    min_events = 5
    max_events = 99
    events_size = 5

    min_day = 14
    max_day = 99
    day_num = 14

    default_size = (
        left_margin + cell_width * min_day + left_margin,
        box_position + (box_height + box_margin) * min_events + bottom_margin,
    )

    bg_color = (255, 255, 255)
    bar_color = (180, 180, 180)
    font_color = (0, 0, 0)
    line_color = (0, 0, 0)
    holiday_color = (210, 210, 210)

    holidays = []

    def __init__(
        self,
        size=default_size,
        color=bg_color,
        today=False,
        firstday=False,
        fix_days=False,
    ):

        self.font_regular = elegantt.utils.detectfont()
        self.font_bold = elegantt.utils.detectfont()

        if today:
            self.today = t(today)
        else:
            self.today = pd.Timestamp.today().normalize()

        if firstday:
            self.firstday = t(firstday)
        else:
            self.firstday = self.today - pd.Timedelta(days=self.today.dayofweek)

        self.resize(
            size=size, color=color, today=today, firstday=firstday, fix_days=fix_days
        )

    def resize(
        self,
        size=default_size,
        color=bg_color,
        today=False,
        firstday=False,
        fix_days=False,
    ):
        self.im = Image.new("RGB", size, color)
        self.draw = ImageDraw.Draw(self.im)

        self.im_width = size[0]
        self.im_height = size[1]

        self.bg_color = color

        if today:
            self.today = t(today)

        if firstday:
            self.firstday = t(firstday)

        if fix_days:
            self.day_num = fix_days

        self.calendar_height = self.im_height - self.top_margin - self.bottom_margin

    def set_holidays(self, holidays):
        self.holidays = holidays

    def get_holidays(self):
        return self.holidays

    def calc_end_date(self, start_date: pd.Timestamp, duration: int):
        custom_business_day = pd.tseries.offsets.CustomBusinessDay(
            holidays=pd.to_datetime(self.holidays)
        )
        return start_date + custom_business_day * (duration - 1)

    def parse_markdown(self, str):
        previous_end_date = t(self.today)
        events = []
        eid = 0
        for line in str.splitlines():
            if "|" in line:
                try:
                    start_date = None
                    end_date = None
                    title = line.split("|")[3].strip()
                    if "---" in title:  # ヘッダ行は読み飛ばす
                        events = []
                        eid = 0
                        title = None

                    dates = re.findall(r"\d{4}-\d{2}-\d{2}", line)
                    duration = re.search(r"\b(\d+)(d)\b", line)
                    if duration:
                        d = int(duration.group(1))

                    if len(dates) == 2:
                        start_date = t(dates[0])
                        end_date = t(dates[1])

                    if len(dates) == 1:
                        start_date = t(dates[0])
                        end_date = self.calc_end_date(start_date, d)

                    if len(dates) == 0 and duration is not None:
                        start_date = self.calc_end_date(
                            previous_end_date, 1 + 1  # 終了日の翌日
                        )
                        end_date = self.calc_end_date(start_date, d)

                    if len(dates) == 0 and duration is None:
                        start_date = None
                        end_date = None
                    else:
                        previous_end_date = end_date

                    if title:
                        events.append(
                            {"title": title, "start": start_date, "end": end_date}
                        )
                        eid = eid + 1
                except Exception as e:
                    print(e)
                    raise
        return events

    def parse_mermaid(self, str):
        previous_end_date = t(self.today)
        events = []
        eid = 0
        for line in str.splitlines():
            if ":" in line:
                try:
                    title = line.split(":")[0].strip()
                    dates = re.findall(r"\d{4}-\d{2}-\d{2}", line)
                    duration = re.search(r"\b(\d+)(d|h)\b", line)
                    if duration:
                        d = int(duration.group(1))

                    if len(dates) == 2:
                        start_date = t(dates[0])
                        end_date = t(dates[1])

                    if len(dates) == 1 and duration is not None:
                        start_date = t(dates[0])
                        end_date = self.calc_end_date(start_date, d)

                    if len(dates) == 1 and duration is None:
                        start_date = t(dates[0])
                        end_date = self.calc_end_date(start_date, 0)

                    if len(dates) == 0 and duration is not None:
                        start_date = self.calc_end_date(
                            previous_end_date, 1 + 1  # 終了日の翌日
                        )
                        end_date = self.calc_end_date(start_date, d)

                    previous_end_date = end_date

                    events.append(
                        {"title": title, "start": start_date, "end": end_date}
                    )
                    eid = eid + 1
                except Exception as e:
                    print(e)
                    raise
            if "section" in line:
                title = line.split("section")[1].strip()
                events.append({"title": title, "start": None, "end": None})
                eid = eid + 1

        return events

    def analyze_events(self, events):

        start = pd.Timestamp.max
        end = pd.Timestamp.min
        size = len(events)
        for event in events:
            if event["start"] and event["start"] < start:
                start = event["start"]
            if event["end"] and event["end"] > end:
                end = event["end"]

        analyzed_events = {"start": start, "end": end, "size": size}
        return analyzed_events

    def auto_resize(self, events, today=False, firstday=False):
        analyzed_events = self.analyze_events(events)

        self.day_num = (analyzed_events["end"] - analyzed_events["start"]).days + 1
        if self.day_num < self.min_day:
            self.day_num = self.min_day
        if self.day_num > self.max_day:
            self.day_num = self.max_day

        self.events_size = analyzed_events["size"]
        if self.events_size < self.min_events:
            self.events_size = self.min_events
        elif self.events_size > self.max_events:
            self.events_size = self.max_events

        if today is None:
            today = analyzed_events["start"].strftime("%Y-%m-%d")

        if firstday is None:
            firstday = analyzed_events["start"].strftime("%Y-%m-%d")

        width = self.calc_width()
        height = self.calc_height()

        self.resize(
            size=(width, height),
            today=today,
            firstday=firstday,
        )

    def auto_draw(self, s: str, mode: str = "mermaid", today=None, firstday=None):

        if mode == "mermaid":
            events = self.parse_mermaid(s)
        if mode == "markdown":
            events = self.parse_markdown(s)

        self.auto_resize(events, today, firstday)
        self.draw_calendar()
        for event in events:
            start = event["start"].strftime("%Y-%m-%d") if event["start"] else None
            end = event["end"].strftime("%Y-%m-%d") if event["end"] else None
            self.draw_campain(start, end, event["title"])

    def calc_height(self, events_size=None):
        if events_size is None:
            events_size = self.events_size
        return (
            events_size * (self.box_height + self.box_margin)
            + self.box_position
            + self.bottom_margin
        )

    def calc_width(self, days=None):
        if days is None:
            days = self.day_num
        return days * self.cell_width + 2 * self.left_margin

    def get_today(self):
        return self.today

    def get_firstday(self):
        return self.firstday

    def set_font(self, regular, bold=False):
        self.font_regular = regular
        if bold:
            self.font_bold = bold
        else:
            self.font_bold = regular

    def get_font(self):
        return self.font_regular

    def set_box_position(self, box_position):
        self.box_position = box_position

    def set_max_day(self, max_day):
        self.max_day = max_day

    def set_bar_height(self, height):
        self.box_height = height

    def set_bar_width(self, width):
        self.cell_width = width

    def set_bar_color(self, color):
        self.bar_color = color

    def set_line_color(self, color):
        self.line_color = color

    def set_holiday_color(self, color):
        self.holiday_color = color

    def set_font_color(self, color):
        self.font_color = color

    def set_font_size(self, size):
        self.font_size = size

    def set_left_margin(self, margin):
        self.left_margin = margin

    def set_top_margin(self, margin):
        self.top_margin = margin

    def set_week_position(self, position):
        self.week_position = position

    def set_date_position(self, position):
        self.date_position = position

    def parse_color_schema(self, schema):
        for k, v in json.loads(schema).items():
            if k == "bg_color":
                self.bg_color = tuple(v)
            if k == "bar_color":
                self.bar_color = tuple(v)
            if k == "font_color":
                self.font_color = tuple(v)
            if k == "line_color":
                self.line_color = tuple(v)
            if k == "holiday_color":
                self.holiday_color = tuple(v)
        self.resize(color=self.bg_color)

    def draw_campain(self, start, end, title):

        if start:
            start_date = t(start)
        else:
            start_date = t("1900-01-01")

        if end:
            end_date = t(end)
        else:
            end_date = t("1900-01-01")

        start_pos = (start_date - self.firstday).days

        if start_pos < 0:
            start_pos = 0

        if end_date > self.firstday:
            end_pos = (end_date - self.firstday).days
        else:
            end_pos = 0

        self.draw.rectangle(
            [
                (
                    start_pos * self.cell_width + self.left_margin,
                    self.box_position + self.num * (self.box_height + self.box_margin),
                ),
                (
                    (end_pos + 1) * self.cell_width + self.left_margin,
                    self.box_position
                    + self.num * (self.box_height + self.box_margin)
                    + self.box_height,
                ),
            ],
            fill=self.bar_color,
            outline=None,
        )

        self.draw.multiline_text(
            (
                start_pos * self.cell_width + self.left_margin + self.font_size / 4,
                self.box_position
                + self.num * (self.box_height + self.box_margin)
                + self.font_size / 2,
            ),
            title,
            fill=self.font_color,
            font=ImageFont.truetype(self.font_regular, self.font_size),
        )
        self.num = self.num + 1

    def draw_calendar(self, days=None):

        week_str = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        # week_str = ['月','火','水','木','金','土','日']

        for i in range(self.day_num):

            d = self.firstday + pd.offsets.DateOffset(n=i)

            if (
                d.weekday() in [5, 6] or d.strftime("%Y-%m-%d") in self.holidays
            ):  # 土日と祝日は背景を灰色にする
                self.draw.rectangle(
                    [
                        (
                            self.left_margin + i * self.cell_width,
                            self.top_margin,
                        ),
                        (
                            self.left_margin + (i + 1) * self.cell_width,
                            self.top_margin + self.calendar_height,
                        ),
                    ],
                    fill=self.holiday_color,
                    outline=None,
                )
            else:
                self.draw.rectangle(
                    [
                        (
                            self.left_margin + i * self.cell_width,
                            self.top_margin - self.font_size,
                        ),
                        (
                            self.left_margin + (i + 1) * self.cell_width,
                            self.top_margin + self.calendar_height,
                        ),
                    ],
                    fill=self.bg_color,
                    outline=None,
                )

            self.draw.line(
                (
                    self.left_margin + i * self.cell_width,
                    self.top_margin,
                    self.left_margin + i * self.cell_width,
                    self.top_margin + self.calendar_height,
                ),
                fill=self.line_color,
                width=1,
            )

            try:
                if d == self.today:
                    font = ImageFont.truetype(self.font_bold, self.font_size)
                else:
                    font = ImageFont.truetype(self.font_regular, self.font_size)
            except OSError:
                raise OSError("font not found")

            self.draw.multiline_text(
                (
                    self.left_margin
                    + i * self.cell_width
                    + self.cell_width / 2
                    - self.font_size / 2,  # 日付は2文字
                    self.date_position,
                ),
                d.strftime("%d"),
                fill=self.font_color,
                font=font,
            )
            self.draw.multiline_text(
                (
                    self.left_margin
                    + i * self.cell_width
                    + self.cell_width / 2
                    - self.font_size,  # 曜日は3文字
                    self.week_position,
                ),
                week_str[d.weekday()],
                fill=self.font_color,
                font=font,
            )

        i = self.day_num
        self.draw.line(
            (
                self.left_margin + i * self.cell_width,
                self.top_margin,
                self.left_margin + i * self.cell_width,
                self.top_margin + self.calendar_height,
            ),
            fill=(0, 0, 0),
            width=1,
        )

    def show(self):
        self.im.show()

    def save(self, fname):
        self.im.save(fname)


if __name__ == "__main__":

    print("example is on github.")
