import sys
import csv

import elegantt


def main(args=sys.argv[1:]):

    fname = args[0]
    data = []
    start_date = "9999-99-99"
    end_date = "0000-00-00"

    if "csv" in fname:
        with open(fname) as csvfile:
            for row in csv.reader(csvfile, delimiter=","):
                data.append(row)
                if row[0] < start_date:
                    start_date = row[0]
                if end_date < row[1]:
                    end_date = row[1]

        gchart = elegantt.EleGantt((720, 320), (255, 255, 255), today=start_date)
        gchart.draw_calendar()
        for row in data:
            gchart.draw_campain(row[0], row[1], row[2])
        gchart.save(fname.replace("csv", "png"))

    if "txt" in fname:
        gchart = elegantt.EleGantt()
        with open(fname) as file:
            content = file.read()
            gchart.auto_draw(content, mode="mermaid")
        gchart.save(fname.replace("txt", "png"))

    if "md" in fname:
        gchart = elegantt.EleGantt()
        with open(fname) as file:
            content = file.read()
            gchart.auto_draw(content, mode="markdown")
        gchart.save(fname.replace("md", "png"))


if __name__ == "__main__":
    main()
