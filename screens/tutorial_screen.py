from graphics import *
from graphics_extras import Button
from game import Game
import webbrowser

WIDTH = 1200
HEIGHT = 800
class TutorialScreen:
    instructions_blackjack = Button(Point(WIDTH / 4 - 50, HEIGHT / 2 - 25), Point(WIDTH / 4 + 50, HEIGHT / 2 + 25), "Start")
    instructions_blackjack.body.setFill("green")


    back_btn = Button(Point(0, 600), Point(200, 700), "Back")
    back_btn.body.setFill("white")

    @staticmethod
    def play_pop(fn):
        Game.pop_sfx.play(loop=False, block=False)
        fn()

    @staticmethod
    def draw_screen(event=None):
        Game.undraw_all()

        TutorialScreen.instructions_blackjack(Game.window)
        TutorialScreen.back_btn.draw(Game.window)

        
        TutorialScreen.instructions_blackjack.bind_click(Game.window, webbrowser.open_new_tab("https://bicyclecards.com/how-to-play/blackjack/"))
        from screens.start_screen import StartScreen
        TutorialScreen.back_btn.bind_click(Game.window, lambda _: TutorialScreen.play_pop(StartScreen.start))
