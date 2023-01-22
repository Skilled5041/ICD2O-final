from graphics import *
from audioplayer import AudioPlayer
from graphics_elements import Button, Slider
import settings.edit_settings as edit_settings
import sys


class Game:
    window = GraphWin("Blackjack", 1200, 800)

    hit_sound = AudioPlayer("sounds/hit_sfx.mp3")
    hit_sound.volume = edit_settings.get_sfx_volume() * 100

    stand_sound = AudioPlayer("sounds/stand_sfx.mp3")
    stand_sound.volume = edit_settings.get_sfx_volume() * 100

    win_sfx = AudioPlayer("sounds/win_sfx.mp3")
    win_sfx.volume = edit_settings.get_sfx_volume() * 100

    lose_sfx = AudioPlayer("sounds/lose_sfx.mp3")
    lose_sfx.volume = edit_settings.get_sfx_volume() * 100

    new_game_sound = AudioPlayer("sounds/new_game.mp3")
    new_game_sound.volume = edit_settings.get_sfx_volume() * 100

    exiting = False

    @staticmethod
    def get_card_image_file(card) -> str:
        # Return the file name of the card image
        value = card.value
        suit = card.get_suit_int()

        values = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
        suits = ["diamonds", "clubs", "hearts", "spades"]

        return f"./cards/{values[value - 1]}_of_{suits[suit - 1]}.png"

    @staticmethod
    def close_win(event=None):
        if Game.exiting:
            return
        Game.exiting = True
        # Animation to make the window transparent
        for i in range(50):
            # Set the transparency of the window
            Game.window.master.attributes("-alpha", 1 - (i * 2) / 100)
            time.sleep(0.01)
        # Exit the program
        sys.exit()

    @staticmethod
    def mainloop():
        Game.window.mainloop()

    # Function to undraw everything in the window
    @staticmethod
    def undraw_all():
        # Loop through all the items in the window that are currently drawn
        for i in range(len(Game.window.items)):
            # Depending on the type of item, undraw it differently (the button I made requires an argument)
            if type(Game.window.items[0]) is Button or type(Game.window.items[0]) is Slider:
                Game.window.items[0].undraw(Game.window)
            elif type(Game.window.items[0]) is not Button or type(Game.window.items[0]) is not Slider:
                Game.window.items[0].undraw()

    window.master.protocol("WM_DELETE_WINDOW", close_win)
