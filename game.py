# A file that contains the functions, variables and objects that are used throughout the entire game

from graphics import *
from audioplayer import AudioPlayer
from graphics_extras import Button, Slider
import settings.edit_settings as edit_settings
import sys


class Game:
    # The game's window
    window = GraphWin("Blackjack", 1200, 800)

    # The sounds used in the game, and the volume is set based on the user's settings (saves between sessions)
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

    pop_sfx = AudioPlayer("sounds/pop_sfx.mp3")
    pop_sfx.volume = edit_settings.get_sfx_volume() * 100

    bgm = AudioPlayer("sounds/background_music_sfx.mp3")
    bgm.volume = edit_settings.get_music_volume() * 100
    # Play the background music and loop it
    bgm.play(loop=True, block=False)

    # Variable to determine if the exiting animation is playing, used to prevent bugs
    exiting = False

    # Takes a card as an argument and returns the file name of the card's image
    @staticmethod
    def get_card_image_file(card) -> str:
        # Get the info of the card
        value = card.value
        suit = card.get_suit_int()

        values = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
        suits = ["diamonds", "clubs", "hearts", "spades"]

        # Return the file name of the card image
        return f"./cards/{values[value - 1]}_of_{suits[suit - 1]}.png"

    # Animation that plays when the close window button is clicked, and then closes the window
    @staticmethod
    def close_win(event=None):
        # If the animation is already playing, don't play it again
        if Game.exiting:
            return
        # Set the variable to true so that the animation doesn't play again
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

    # Make it so when the close window button is clicked, the animation is played
    window.master.protocol("WM_DELETE_WINDOW", close_win)
