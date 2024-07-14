import csv
import fire
import sys

import elegantt


def main(fname=False, out=False):

    if fname is False:
        print("usage: elegantt --fname path/to/file")
        sys.exit()

    data = []
    start_date = "9999-99-99"
    end_date = "0000-00-00"

    try:
        with open(fname) as file:

            if "csv" in fname:
                if out is False:
                    out = fname.replace("csv", "png")
                for row in csv.reader(file, delimiter=","):
                    data.append(row)
                    if row[0] < start_date:
                        start_date = row[0]
                    if end_date < row[1]:
                        end_date = row[1]
                gchart = elegantt.EleGantt(today=start_date)
                gchart.draw_calendar()
                for row in data:
                    gchart.draw_campain(row[0], row[1], row[2])
            if "txt" in fname:
                if out is False:
                    out = fname.replace("txt", "png")
                gchart = elegantt.EleGantt()
                content = file.read()
                gchart.auto_draw(content, mode="mermaid")
            if "md" in fname:
                if out is False:
                    out = fname.replace("md", "png")
                gchart = elegantt.EleGantt()
                content = file.read()
                gchart.auto_draw(content, mode="markdown")
            gchart.save(out)
    except FileNotFoundError as e:
        print(e)
        # raise
    except Exception as e:
        print(e)


def main2():
    fire.Fire(main)


if __name__ == "__main__":
    fire.Fire(main)
