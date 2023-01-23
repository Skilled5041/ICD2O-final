from graphics import *
from graphics_extras import Button
from screens.stats_screen import StatsScreen
from game import Game
import time

# Constants for the window width and height
WIDTH = 1200
HEIGHT = 800

class StartScreen:
    # Set the background color of the window
    Game.window.setBackground(color_rgb(166, 208, 240))

    # Create the left sidebar as a Polygon object and set its fill color
    sidebar1 = Polygon(Point(0, 0), Point(WIDTH / 8, HEIGHT / 8), Point(WIDTH / 10, HEIGHT), Point(0, HEIGHT))
    sidebar1.setFill(color_rgb(91, 177, 243))

    # Create the right sidebar as a Polygon object and set its fill color
    sidebar2 = Polygon(Point(WIDTH, 0), Point(7 * WIDTH / 8, HEIGHT / 8), Point(9 * WIDTH / 10, HEIGHT),
                       Point(WIDTH, HEIGHT))
    sidebar2.setFill(color_rgb(91, 177, 243))

    # Create the title text and set its text color and size
    title = Text(Point(WIDTH / 2, HEIGHT / 4), "Welcome to our game!")
    title.setSize(32)
    title.setTextColor("white")

    # Create the "Start" button and set its fill color
    start_button = Button(Point(WIDTH / 4 - 50, HEIGHT / 2 - 25), Point(WIDTH / 4 + 50, HEIGHT / 2 + 25), "Start")
    start_button.body.setFill("green")

    # Create the "Tutorial" button and set its fill color
    tutorial_button = Button(Point(WIDTH / 2 - 50, HEIGHT / 2 - 25), Point(WIDTH / 2 + 50, HEIGHT / 2 + 25), "Tutorial")
    tutorial_button.body.setFill("blue")

    # Create the "Stats" button and set its fill color
    stats_button = Button(Point(3 * WIDTH / 4 - 50, HEIGHT / 2 - 25), Point(3 * WIDTH / 4 + 50, HEIGHT / 2 + 25), "Stats")
    stats_button.body.setFill("red")

    # Create the three lines
    line_left = Line(Point(145, 310), Point(180, 240))
    line_right = Line(Point(1030, 240), Point(1055, 310))
    line_middle = Line(Point(180, 240), Point(1030, 240))

    # Set the width of the lines
    line_right.setWidth(5)
    line_left.setWidth(5)
    line_middle.setWidth(5)

    # Create the "Settings" button and set its fill color
    settings_btn = Button(Point(1100, 50), Point(1200, 100), "Settings")
    settings_btn.body.setFill("yellow")

    # Create the names text and set its size
    names = Text(Point(WIDTH / 2, HEIGHT / 2 + 200), "Made by Aaron and Calvin")
    names.setSize(32)

    #method to draw buttons and lines to the window
    @staticmethod
    def draw_screen(event=None):
        StartScreen.sidebar1.draw(Game.window)
        StartScreen.sidebar2.draw(Game.window)
        StartScreen.title.draw(Game.window)
        StartScreen.start_button.draw(Game.window)
        StartScreen.tutorial_button.draw(Game.window)
        StartScreen.stats_button.draw(Game.window)
        StartScreen.line_left.draw(Game.window)
        StartScreen.line_right.draw(Game.window)
        StartScreen.line_middle.draw(Game.window)
        StartScreen.settings_btn.draw(Game.window)
        StartScreen.names.draw(Game.window)

        Game.window.setBackground(color_rgb(166, 208, 240))
        StartScreen.start_button.body.setFill("green")
        StartScreen.tutorial_button.body.setFill("blue")
        StartScreen.stats_button.body.setFill("red")
        StartScreen.settings_btn.body.setFill("yellow")
    #method to animate sidebars
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
#method to fade out buttons, sidebars, and text
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
            StartScreen.settings_btn.body.setFill(color_rgb(255 - i * 25, 255 - i * 25, 0))
            StartScreen.title.setTextColor(color_rgb(255 - i * 25, 255 - i * 25, 255 - i * 25))
            update(30)
        StartScreen.settings_btn.undraw(Game.window)

        for i in range(10):
            StartScreen.title.setTextColor(color_rgb(255 - i * 25, 255 - i * 25, 255 - i * 25))
            update(30)

        for i in range(10):
            StartScreen.title.setTextColor(color_rgb(255 - i * 25, 255 - i * 25, 255 - i * 25))
            update(30)
        StartScreen.title.undraw()

        for i in range(10):
            StartScreen.names.setTextColor(color_rgb(255 - i * 25, 255 - i * 25, 255 - i * 25))
            update(30)
        StartScreen.names.undraw()

        for i in range(int(WIDTH / 2), 0, -10):
            rectangle1 = Rectangle(Point(i, 0), Point(i + 10, HEIGHT))
            rectangle1.setFill("white")
            rectangle1.draw(Game.window)
            rectangle2 = Rectangle(Point(WIDTH - i - 10, 0), Point(WIDTH - i, HEIGHT))
            rectangle2.setFill("white")
            rectangle2.draw(Game.window)
            update(100)

        Game.undraw_all()
    #method to switch the screens
    @staticmethod
    def switch_to_choose_game_screen(event=None):
        Game.pop_sfx.play(loop=False, block=False)
        StartScreen.fade_out()
        from screens.choose_game_screen import ChooseGameScreen
        ChooseGameScreen.draw_screen()
#play the pop sound on click
    @staticmethod
    def play_pop(fn):
        Game.pop_sfx.play(loop=False, block=False)
        fn()
#method to start a game
    @staticmethod
    def start(event=None):
        Game.undraw_all()

        StartScreen.draw_screen()
        StartScreen.animate()

        StartScreen.start_button.bind_click(Game.window, StartScreen.switch_to_choose_game_screen)
        StartScreen.stats_button.bind_click(Game.window, lambda _: StartScreen.play_pop(StatsScreen.draw_screen))
        from screens.settings_screen import SettingsScreen
        StartScreen.settings_btn.bind_click(Game.window, lambda _: StartScreen.play_pop(SettingsScreen.draw_screen))
        from screens.tutorial_screen import TutorialScreen
        StartScreen.tutorial_button.bind_click(Game.window, lambda _: StartScreen.play_pop(TutorialScreen.draw_screen))
