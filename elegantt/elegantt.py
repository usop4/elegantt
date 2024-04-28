#!python3
# -*- coding: utf-8 -*-

import datetime
import sys
import random
import os
from PIL import Image, ImageDraw, ImageFont

import elegantt.utils

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
    bar_color = (128,128,128)
    font_color = (0,0,0)
    line_color = (0,0,0)
    holiday_color = (220,220,220)
    max_day = 14
 
    def __init__(self,size=(512,256),color=(255,255,255),today=False):
        self.im = Image.new("RGB",size,color) #(512, 256), (255, 255, 255)
        self.draw = ImageDraw.Draw(self.im)

        self.im_width = size[0]
        self.im_height = size[1]

        self.bg_color = color

        if today:
            self.today = datetime.date.fromisoformat(today)
        else:
            self.today = datetime.date.today()

        self.monday = self.today - datetime.timedelta(days=self.today.weekday())

        self.calendar_height = size[1] - self.top_margin - self.bottom_margin

        self.font_regular = elegantt.utils.detectfont()
        self.font_bold = elegantt.utils.detectfont()


    def set_font(self,regular,bold=False):
        self.font_regular = regular
        if bold:
            self.font_bold = bold
        else:
            self.font_bold = regular

    def get_monday(self):
        return self.monday

    def set_box_position(self,box_position):
        self.box_position = box_position

    def set_max_day(self,max_day):
        self.max_day = max_day

    def set_bar_height(self,height):
        self.box_height = height

    def set_bar_width(self,width):
        self.cell_width = width
    
    def set_bar_color(self,color):
        self.bar_color = color

    def set_line_color(self,color):
        self.line_color = color

    def set_holiday_color(self,color):
        self.holiday_color = color

    def set_font_color(self,color):
        self.font_color = color

    def set_font_size(self,size):
        self.font_size = size

    def set_left_margin(self,margin):
        self.left_margin = margin

    def set_top_margin(self,margin):
        self.top_margin = margin

    def set_week_position(self,position):
        self.week_position = position

    def set_date_position(self,position):
        self.date_position = position

    def draw_campain(self,start,end,title):

        start_date = datetime.datetime.strptime(start,'%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end,'%Y-%m-%d').date()

        start_pos = (start_date - self.monday).days
        if start_pos < 0:
            start_pos = 0
        if start_pos > self.max_day:
            start_pos = self.max_day
        end_pos = (end_date - self.monday).days
        if end_pos > self.max_day:
            end_pos = self.max_day -1

        self.draw.rectangle(
            [
                (
                    start_pos * self.cell_width + self.left_margin,
                    self.box_position + self.num * (self.box_height+self.box_margin)
                ),
                (
                    (end_pos+1) * self.cell_width + self.left_margin,
                    self.box_position + self.num * (self.box_height+self.box_margin) + self.box_height
                )
            ],
            fill = self.bar_color,
            outline = None
        )
        self.draw.multiline_text(
            (
                start_pos * self.cell_width + self.left_margin + self.font_size/4,
                self.box_position + self.num * (self.box_height+self.box_margin) + self.font_size/2
            ),
            title,
            fill = self.font_color, 
            font = ImageFont.truetype(self.font_regular, self.font_size)
        )
        self.num = self.num + 1

    def draw_calendar(self):

        week_str = ['Mon ','Tue','Wed','Thu','Fri','Sat','Sun']
        #week_str = ['月','火','水','木','金','土','日']

        for i in range(self.max_day):
            
            d = self.monday+datetime.timedelta(days=i)

            if d.weekday() in [5,6]: #土日は背景を灰色にする
                self.draw.rectangle(
                    [
                        (
                            self.left_margin + i*self.cell_width,
                            self.top_margin - self.font_size
                        ),
                        (
                            self.left_margin + (i+1)*self.cell_width,
                            self.top_margin + self.calendar_height
                        )
                    ],
                    fill = self.holiday_color,
                    outline = None
                )
            else:
                self.draw.rectangle(
                    [
                        (
                            self.left_margin + i*self.cell_width,
                            self.top_margin - self.font_size
                        ),
                        (
                            self.left_margin + (i+1)*self.cell_width,
                            self.top_margin + self.calendar_height
                        )
                    ],
                    fill = self.bg_color,
                    outline = None
                )

            self.draw.line(
                (
                    self.left_margin + i*self.cell_width, 
                    self.top_margin,
                    self.left_margin + i*self.cell_width, 
                    self.top_margin + self.calendar_height),
                fill = self.line_color,
                width = 1
            )

            if d == self.today:
                font = ImageFont.truetype(self.font_bold, self.font_size)
            else:
                font = ImageFont.truetype(self.font_regular, self.font_size)

            self.draw.multiline_text(
                (
                    self.left_margin + i*self.cell_width + self.cell_width/2 - self.font_size/2,
                    self.date_position
                ),
                d.strftime('%d'),
                fill=self.font_color, 
                font=font
            )
            self.draw.multiline_text(
                (
                    self.left_margin + i*self.cell_width + self.cell_width/2 - self.font_size/2,
                    self.week_position
                ),
                week_str[i%7],
                fill=self.font_color, 
                font=font
            )

        i = self.max_day
        self.draw.line(
            (
                self.left_margin + i*self.cell_width, 
                self.top_margin,
                self.left_margin + i*self.cell_width, 
                self.top_margin + self.calendar_height
            ),
            fill = (0,0,0),
            width = 1
        )

    def show(self):
        self.im.show()

    def save(self,fname):
        self.im.save(fname)

    def draw_random_line(self):
        for x in range(self.im_width):
            self.draw.line(
                (
                    x, 0, x, self.im_height
                ),
                fill = (
                    random.randrange(0,100),
                    random.randrange(0,100),
                    random.randrange(0,30)
                ),
                width = 1
            )


if __name__ == '__main__':

    print("example is on github.")
