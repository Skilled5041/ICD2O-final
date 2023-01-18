from graphics import *
from graphics_elements import Button
from audioplayer import AudioPlayer


class Game:
    window = GraphWin("Blackjack", 1200, 800)

    close_btn = Button(Point(0, 0), Point(30, 30), "X")
    close_btn.body.setFill("red")
    close_btn.body.setOutline("red")

    hitsound = AudioPlayer("./sounds/hit_sfx.mp3")
    standsound = AudioPlayer("./sounds/stand_sfx.mp3")
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
        for i in range(100):
            # Set the transparency of the window
            Game.window.master.attributes("-alpha", 1 - i / 100)
            time.sleep(0.01)
        # Exit the program
        sys.exit()

    @staticmethod
    def mainloop():
        Game.window.mainloop()
