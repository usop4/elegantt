# elegantt

## Overview

elegantt is gantt chart drawing library.

## Usage

```
gchart = elegantt.EleGantt( (720, 320),(255,255,255),today="2019-10-15")
gchart.set_font('ipaexg/ipaexg.ttf')
gchart.draw_calendar()
gchart.draw_campain("2019-10-15","2019-10-18","こんにちは")
gchart.draw_campain("2019-10-20","2019-10-23","こんにちは")
gchart.draw_campain("2019-10-24","2019-10-30","こんにちは")
gchart.save("test_basic_1.png")
```

# Lisence

This project is licensed under the MIT License, see the LICENSE.txt file for details

