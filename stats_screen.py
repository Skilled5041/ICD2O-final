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
    def reset_stats(event=None) -> None:
        edit_stats.reset()
        stats.setText(f"Games played: 0\n"
                      f"Wins: 0\n"
                      f"Losses: 0\n"
                      f"Win rate: 0.00%\n"
                      f"Time played: 0 seconds")

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

    with open("stats.json", "r") as files:
        data = json.load(files)

    stats = Text(Point(600, 500), f"Games played: {data['games_played']}\n"
                                  f"Wins: {data['wins']}\n"
                                  f"Losses: {data['losses']}\n"
                                  f"Win rate: {(data['win-rate'] * 100):.2f}%\n"
                                  f"Time played: {secondsToStr(data['total_time'])}")
    stats.setSize(24)
    stats.draw(window)
