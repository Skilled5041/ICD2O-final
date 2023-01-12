import edit_stats
import json
from graphics import *
from graphics_elements import Button


def secondsToStr(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 60 * 60:
        return f"{seconds // 60} minutes and {seconds % 60} seconds"
    elif seconds < 60 * 60 * 24:
        return f"{seconds // (60 * 60)} hours and {(seconds // 60) % 60} minutes"
    else:
        return f"{seconds // (60 * 60 * 24)} days and {(seconds // (60 * 60)) % 24} hours ({seconds // (60 * 60)} hours)"


def stats_screen(window):
    def stats_as_string() -> str:
        string = ""
        with open("stats.json") as file:
            data = json.load(file)

        for key in data:
            if key == "win-rate":
                string += f"win-rate: {data[key] * 100:.2f}%\n"
            elif key == "total_time":
                string += f"total time: {secondsToStr(data[key])}\n"
            else:
                string += f"{key.replace('_', ' ')}: {data[key]}\n"

        return string

    def reset_stats(event=None) -> None:
        edit_stats.reset()
        stats.setText(stats_as_string())

    bg = Image(Point(600, 400), "images/stats_bg.png")
    bg.draw(window)

    back_btn = Button(Point(200, 700), Point(0, 600), "Back")
    back_btn.body.setFill("white")
    back_btn.label.setSize(24)
    back_btn.draw(window)

    reset_btn = Button(Point(1000, 450), Point(1200, 550), "Reset Stats")
    reset_btn.body.setFill("white")
    reset_btn.label.setSize(24)
    reset_btn.draw(window)
    reset_btn.bind_click(window, reset_stats)

    title = Text(Point(600, 300), "Stats")
    title.setSize(36)
    title.draw(window)

    stats = Text(Point(600, 500), stats_as_string())
    stats.setSize(24)
    stats.draw(window)
