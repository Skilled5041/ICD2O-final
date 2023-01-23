from graphics import *
from graphics_extras import Button
from game import Game
import webbrowser

#sets tutorial screen class, buttons, and size of text
class TutorialScreen:
    instructions_blackjack = Button(Point(400, 200), Point(800, 400), "Click for Blackjack Game Rules")
    instructions_blackjack.body.setFill("green")
    instructions_blackjack.label.setSize(20)
    instructions_slapjack = Button(Point(400, 500), Point(800, 700), "Click for Slapjack Game Rules")
    instructions_slapjack.body.setFill("blue")
    instructions_slapjack.label.setSize(20)
    instructions_slapjack.label.setTextColor("white")

    back_btn = Button(Point(0, 600), Point(200, 700), "Back")
    back_btn.body.setFill("white")
#plays the pop sound on a click

    @staticmethod
    def play_pop(fn):
        Game.pop_sfx.play(loop=False, block=False)
        fn()
#static method to open a link        
    @staticmethod
    def open_link(link):
        webbrowser.open_new_tab(link)
#static method to draw things to a sreen
    @staticmethod
    def draw_screen(event=None):
        Game.undraw_all()

        TutorialScreen.instructions_blackjack.draw(Game.window)
        TutorialScreen.back_btn.draw(Game.window)
        TutorialScreen.instructions_slapjack.draw(Game.window)

        TutorialScreen.instructions_blackjack.bind_click(Game.window, lambda _: TutorialScreen.open_link(
            "https://bicyclecards.com/how-to-play/blackjack/"))
        TutorialScreen.instructions_slapjack.bind_click(Game.window, lambda _: TutorialScreen.open_link(
            "https://bicyclecards.com/how-to-play/slapjack/"))

        from screens.start_screen import StartScreen
        TutorialScreen.back_btn.bind_click(Game.window, lambda _: TutorialScreen.play_pop(StartScreen.start))
