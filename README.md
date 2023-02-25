# elegantt

## Overview

elegantt is gantt chart drawing library.

## Install 

```pip install elegantt```

## Fonts Install

on Ubuntsu
```apt install fonts-noto-cjk```

on RedHat/RockyLinux
```yum install google-noto-sans-cjk-ttc-fonts.noarch```

## Usage

ad command line

```eleteng sample.csv```


as library

```
import elegantt
chartsize = (720,320)
bgcolor = (255,255,255)
gchart = elegantt.EleGantt( chartsize, bgcolor, today="2019-10-15")
gchart.draw_calendar()
gchart.draw_campain("2019-10-15","2019-10-18","こんにちは")
gchart.draw_campain("2019-10-20","2019-10-23","こんにちは")
gchart.draw_campain("2019-10-24","2019-10-30","こんにちは")
gchart.save("test_basic_1.png")
```

# Lisence

This project is licensed under the MIT License, see the LICENSE.txt file for details

