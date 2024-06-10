![PyPI - Version](https://img.shields.io/pypi/v/elegantt)
[![Downloads](https://static.pepy.tech/badge/elegantt)](https://pepy.tech/project/elegantt)


# elegantt

## Overview

elegantt is gantt chart drawing library designed for developers and project managers who need to visualize project timeline efficiently. With support for both CSV and Mermaid formats. elegantt provides the flexibility and functionality you need to keep your projects on task.

## Features

- Simpe and intuitive API
- Supports both CSV and Mermaid Gantt chart formats
- customizable chat size and colors
- Command line interface for quick usage
- Cross-platform support

## Installation

Install elegantt via pip:
```sh
pip install elegantt
```

## Fonts Installation

To ensure proper rendering of text, install the necessary fonts:

on Ubuntsu
```sh
apt install fonts-noto-cjk
```

on RedHat/RockyLinux
```sh
yum install google-noto-sans-cjk-ttc-fonts.noarch
```

## Usage

### Command Line interface

Generate a Gantt chart from CSV file:

```sh
eletentt sample.csv
```

CSV Format Example

```txt
2023-01-01,2023-01-04,Task 1
2023-01-02,2023-01-05,Task 2
2023-01-04,2023-01-06,Task 3
```

generate a Gantt chart from a Mermaid format:

```sh
eletentt sample_mermaid.txt
```

Mermaid Format Example

```
gantt
    section task a
    task b            :active,  des2, 2024-05-20, 4d
    task c            :         des3, after des2, 7d
```

generate a Gantt chart from a Mermaid format:

```sh
eletentt sample_markdown.md
```

Markdown Format Example

```
|2024-06-15|2024-06-18|task a|
|2024-06-20|2d        |task b|
|3d        |          |task c|
```

### As a library

integrate elegantt into your python projects for advanced usage:

```py
import elegantt

# Define chart properties
chartsize = (720,320)
bgcolor = (255,255,255)

# Create a Gant chart object
gchart = elegantt.EleGantt( chartsize, bgcolor, today="2019-10-15")

# Draw calendar and campains
gchart.draw_calendar()
gchart.draw_campain("2019-10-15","2019-10-18","Task 1")
gchart.draw_campain("2019-10-20","2019-10-23","Task 2")
gchart.draw_campain("2019-10-24","2019-10-30","Task 3")
gchart.save("gantt_chart.png")
```

or auto_draw for mermaid or markdown format

```py
import elegantt

s = """
    task a  :done, des1, 2024-06-15, 2024-06-18
    task b  :active, des2, 2024-06-20, 2d
    task c  :         des3, after des2, 3d
"""
gchart = elegantt.EleGantt(today="2024-06-18")
gchart.auto_draw(s, mode="mermaid")
gchart.save("gantt_chart.png")
```

## Lisence

This project is licensed under the MIT License, see the LICENSE.txt file for details

## Contributing

We welcome contributions!

## Support

For support or any questions, feel free to open an issue on our Github page.


