from graphics import *
from game import Game


class TutorialScreen:
    instructions_text = Text(Point(600, 200), "The goal of the game is to have a hand value of 21 or as close to 21 as "
                                              "possible without going over (busting).\nThe value of the cards is as "
                                              "follows: 2-10 are face value, aces can be 1 or 11, and face cards ("
                                              "kings, queens, and jacks) are worth 10.\nAfter receiving your initial "
                                              "two cards, you have the option to \"hit\" and receive additional cards "
                                              "to try and improve your hand, one at a time.\nOnce you are satisfied "
                                              "with your hand, you can \"stand\" and keep your current hand\nThe "
                                              "dealer will then reveal their second card and play according to a set "
                                              "of rules that dictate when they must hit and when they must stand.\nIf "
                                              "the dealer busts (goes over 21), all remaining players win.\nIf the "
                                              "dealer does not bust, then the player's hands are compared to the "
                                              "dealer's hand and whoever has the hand closest to 21 without going over "
                                              "wins.")

    instructions_text.setSize(10)

    @staticmethod
    def draw_screen(event=None):
        Game.undraw_all()

        TutorialScreen.instructions_text.draw(Game.window)
