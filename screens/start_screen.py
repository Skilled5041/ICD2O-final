from graphics import *
from graphics_elements import Button
from screens.stats_screen import StatsScreen
from screens.blackjack_game import BlackjackGame
from game import Game
import time

WIDTH = 1200
HEIGHT = 800


class StartScreen:
    Game.window.setBackground(color_rgb(166, 208, 240))

    sidebar1 = Polygon(Point(0, 0), Point(WIDTH / 8, HEIGHT / 8), Point(WIDTH / 10, HEIGHT), Point(0, HEIGHT))
    sidebar1.setFill(color_rgb(91, 177, 243))

    sidebar2 = Polygon(Point(WIDTH, 0), Point(7 * WIDTH / 8, HEIGHT / 8), Point(9 * WIDTH / 10, HEIGHT),
                       Point(WIDTH, HEIGHT))
    sidebar2.setFill(color_rgb(91, 177, 243))

    title = Text(Point(WIDTH / 2, HEIGHT / 4), "Welcome to Blackjack!")
    title.setSize(32)
    title.setTextColor("white")

    start_button = Button(Point(WIDTH / 4 - 50, HEIGHT / 2 - 25), Point(WIDTH / 4 + 50, HEIGHT / 2 + 25), "Start")
    start_button.body.setFill("green")

    tutorial_button = Button(Point(WIDTH / 2 - 50, HEIGHT / 2 - 25), Point(WIDTH / 2 + 50, HEIGHT / 2 + 25), "Tutorial")
    tutorial_button.body.setFill("blue")

    stats_button = Button(Point(3 * WIDTH / 4 - 50, HEIGHT / 2 - 25), Point(3 * WIDTH / 4 + 50, HEIGHT / 2 + 25), "Stats")
    stats_button.body.setFill("red")

    line_left = Line(Point(145, 310), Point(180, 240))
    line_right = Line(Point(1030, 240), Point(1055, 310))
    line_middle = Line(Point(180, 240), Point(1030, 240))

    line_right.setWidth(5)
    line_left.setWidth(5)
    line_middle.setWidth(5)

    @staticmethod
    def draw_screen():
        StartScreen.sidebar1.draw(Game.window)
        StartScreen.sidebar2.draw(Game.window)
        StartScreen.title.draw(Game.window)
        StartScreen.start_button.draw(Game.window)
        StartScreen.tutorial_button.draw(Game.window)
        StartScreen.stats_button.draw(Game.window)
        StartScreen.line_left.draw(Game.window)
        StartScreen.line_right.draw(Game.window)
        StartScreen.line_middle.draw(Game.window)

    @staticmethod
    def animate():
        for i in range(37):
            time.sleep(0.01)
            StartScreen.sidebar1.move(20, 0)
            StartScreen.sidebar2.move(-20, 0)

        for i in range(37):
            time.sleep(0.01)
            StartScreen.sidebar1.move(-20, 0)
            StartScreen.sidebar2.move(20, 0)

    @staticmethod
    def fade_out(event=None):
        for i in range(10):
            StartScreen.start_button.body.setFill(color_rgb(0, 255 - i * 25, 0))
            StartScreen.title.setTextColor(color_rgb(255 - i * 25, 255 - i * 25, 255 - i * 25))
            update(30)
        StartScreen.start_button.undraw(Game.window)

        for i in range(10):
            StartScreen.tutorial_button.body.setFill(color_rgb(0, 0, 255 - i * 25))
            StartScreen.title.setTextColor(color_rgb(255 - i * 25, 255 - i * 25, 255 - i * 25))
            update(30)
        StartScreen.tutorial_button.undraw(Game.window)

        for i in range(10):
            StartScreen.stats_button.body.setFill(color_rgb(255 - i * 25, 0, 0))
            StartScreen.title.setTextColor(color_rgb(255 - i * 25, 255 - i * 25, 255 - i * 25))
            update(30)
        StartScreen.stats_button.undraw(Game.window)

        for i in range(10):
            StartScreen.title.setTextColor(color_rgb(255 - i * 25, 255 - i * 25, 255 - i * 25))
            update(30)

        for i in range(10):
            StartScreen.title.setTextColor(color_rgb(255 - i * 25, 255 - i * 25, 255 - i * 25))
            update(30)
        StartScreen.title.undraw()

        for i in range(int(WIDTH / 2), 0, -10):
            rectangle1 = Rectangle(Point(i, 0), Point(i + 10, HEIGHT))
            rectangle1.setFill("white")
            rectangle1.draw(Game.window)
            rectangle2 = Rectangle(Point(WIDTH - i - 10, 0), Point(WIDTH - i, HEIGHT))
            rectangle2.setFill("white")
            rectangle2.draw(Game.window)
            update(100)

        Game.undraw_all()

    @staticmethod
    def switch_to_blackjack(event=None):
        StartScreen.fade_out()
        BlackjackGame.draw_screen()
        BlackjackGame.start_new_game()

    @staticmethod
    def start(event=None):
        Game.undraw_all()

        StartScreen.draw_screen()
        StartScreen.animate()

        StartScreen.start_button.bind_click(Game.window, StartScreen.switch_to_blackjack)
        StartScreen.stats_button.bind_click(Game.window, StatsScreen.draw_screen)