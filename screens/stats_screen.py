from stats import edit_stats
import json
from graphics import *
from graphics_elements import Button
from game import Game


def secondsToStr(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 60 * 60:
        return f"{seconds // 60} minutes and {seconds % 60} seconds"
    elif seconds < 60 * 60 * 24:
        return f"{seconds // (60 * 60)} hours and {(seconds // 60) % 60} minutes"
    else:
        return f"{seconds // (60 * 60 * 24)} days and {(seconds // (60 * 60)) % 24} hours ({seconds // (60 * 60)} hours)"


class StatsScreen:
    @staticmethod
    def stats_as_string() -> str:
        string = ""
        with open("./stats/stats.json") as file:
            data = json.load(file)

        for key in data:
            if key == "win-rate":
                string += f"win-rate: {data[key] * 100:.2f}%\n"
            elif key == "total_time":
                string += f"total time: {secondsToStr(data[key])}\n"
            else:
                string += f"{key.replace('_', ' ')}: {data[key]}\n"

        return string

    @staticmethod
    def reset_stats(event=None) -> None:
        edit_stats.reset()
        StatsScreen.stats.setText(StatsScreen.stats_as_string())

    bg = Image(Point(600, 400), "images/stats_bg.png")

    back_btn = Button(Point(200, 700), Point(0, 600), "Back")
    back_btn.body.setFill("white")
    back_btn.label.setSize(24)

    reset_btn = Button(Point(1000, 450), Point(1200, 550), "Reset Stats")
    reset_btn.body.setFill("white")
    reset_btn.label.setSize(24)

    title = Text(Point(600, 300), "Stats")
    title.setSize(36)

    stats = Text(Point(600, 500), stats_as_string())
    stats.setSize(24)

    @staticmethod
    def play_pop(fn):
        Game.pop_sfx.play(block=False, loop=False)
        fn()

    @staticmethod
    def draw_screen(event=None):
        Game.undraw_all()

        StatsScreen.bg.draw(Game.window)
        StatsScreen.back_btn.draw(Game.window)
        StatsScreen.reset_btn.draw(Game.window)
        StatsScreen.title.draw(Game.window)
        StatsScreen.stats.draw(Game.window)

        StatsScreen.stats.setText(StatsScreen.stats_as_string())

        StatsScreen.reset_btn.bind_click(Game.window, lambda _: StatsScreen.play_pop(StatsScreen.reset_stats))
        from screens.start_screen import StartScreen
        StatsScreen.back_btn.bind_click(Game.window, lambda _: StatsScreen.play_pop(StartScreen.start))
