from graphics import *
from graphics_elements import Button
from screens.blackjack_game import BlackjackGame
from screens.start_screen import StartScreen
from game import Game


class ChooseGameScreen:

    title_text = Text(Point(600, 250), "Choose A Game To Play")
    title_text.setSize(36)

    blackjack_button = Button(Point(400, 350), Point(800, 450), "Blackjack")
    blackjack_button.body.setFill(color_rgb(255, 255, 255))
    blackjack_button.label.setFill(color_rgb(0, 0, 0))
    blackjack_button.label.setSize(24)

    slapjack_button = Button(Point(400, 500), Point(800, 600), "Slapjack")
    slapjack_button.body.setFill(color_rgb(255, 255, 255))
    slapjack_button.label.setFill(color_rgb(0, 0, 0))
    slapjack_button.label.setSize(24)

    back_button = Button(Point(400, 650), Point(800, 750), "Back")
    back_button.body.setFill(color_rgb(255, 255, 255))
    back_button.label.setFill(color_rgb(0, 0, 0))
    back_button.label.setSize(24)

    @staticmethod
    def play_pop(fn):
        Game.pop_sfx.play(block=False, loop=False)
        fn()

    @staticmethod
    def draw_screen():
        Game.undraw_all()
        Game.window.setBackground(color_rgb(89, 191, 255))

        ChooseGameScreen.title_text.draw(Game.window)
        ChooseGameScreen.blackjack_button.draw(Game.window)
        ChooseGameScreen.slapjack_button.draw(Game.window)
        ChooseGameScreen.back_button.draw(Game.window)

        ChooseGameScreen.blackjack_button.bind_click(Game.window, ChooseGameScreen.switch_to_blackjack)
        ChooseGameScreen.back_button.bind_click(Game.window, lambda _: ChooseGameScreen.play_pop(StartScreen.start))

    @staticmethod
    def switch_to_blackjack(event=None):
        Game.pop_sfx.play(block=False, loop=False)
        BlackjackGame.draw_screen()
        BlackjackGame.start_new_game()
