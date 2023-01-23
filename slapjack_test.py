from graphics import *
from graphics_extras import Button
import random


class WinWindow:
    def __init__(self, window):
        self.window = window
        self.window.setBackground(color_rgb(113, 203, 255))
        self.win_message = Text(Point(600, 200), "Congrats, you won!")
        self.win_message.setStyle('bold')
        self.win_message.setSize(36)
        self.win_message.draw(self.window)

        self.new_game_btn = Button(Point(250, 400), Point(450, 500), "New Game")
        self.new_game_btn.body.setFill("green")
        self.new_game_btn.label.setSize(24)
        self.new_game_btn.draw(self.window)

        self.main_menu_btn = Button(Point(750, 400), Point(950, 500), "Quit")
        self.main_menu_btn.body.setFill("red")
        self.main_menu_btn.label.setSize(24)
        self.main_menu_btn.draw(self.window)

    def check_buttons(self):
        if not self.window.isClosed():
            while True:
                click1 = self.window.getMouse()
                if self.new_game_btn.inside(click1):
                    self.window.close()
                    main()
                if self.main_menu_btn.inside(click1):
                    quit_text = Text(Point(600, 600), "Quitting the game...")
                    quit_text.setSize(20)
                    quit_text.draw(self.window)
                    time.sleep(1)
                    sys.exit()


class LoseWindow:
    def __init__(self, window):
        self.window = window
        self.window.setBackground(color_rgb(255, 204, 203))

        self.lost_message = Text(Point(600, 200), "You Lost :(")
        self.lost_message.setStyle('bold')
        self.lost_message.setSize(36)
        self.lost_message.draw(self.window)

        self.new_game_btn = Button(Point(250, 400), Point(450, 500), "New Game")
        self.new_game_btn.body.setFill("green")
        self.new_game_btn.label.setSize(24)
        self.new_game_btn.draw(self.window)

        self.main_menu_btn = Button(Point(750, 400), Point(950, 500), "Quit")
        self.main_menu_btn.body.setFill("red")
        self.main_menu_btn.label.setSize(24)
        self.main_menu_btn.draw(self.window)

    def check_buttons(self):
        if not self.window.isClosed():
            if self.new_game_btn.bind_click(self.window, lambda *args: None):
                self.window.close()
                main()
            if self.main_menu_btn.bind_click(self.window, lambda *args: None):
                quit_text = Text(Point(600, 600), "Quitting the game...")
                quit_text.setSize(20)
                quit_text.draw(self.window)
                time.sleep(1)
                sys.exit()


class RandomCard:
    def __init__(self):
        self.suits = ["spades", "diamonds", "hearts", "clubs"]
        self.values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
        self.suit = random.choice(self.suits)
        self.value = random.choice(self.values)

    def generate(self):
        return f"./cards/{self.value}_of_{self.suit}.png", self.value


class DisplayCard:
    def __init__(self, card_file, window):
        self.card_file = card_file
        self.window = window
        self.card_image = Image(Point(600, 250), self.card_file)
        self.card_image.draw(self.window)


class Main:
    def __init__(self):
        self.win = GraphWin("Slapjack", 1200, 800)
        self.reveal_button = Button(Point(250, 550), Point(550, 700), "REVEAL")
        self.reveal_button.body.setFill("green")
        self.reveal_button.label.setSize(24)
        self.reveal_button.draw(self.win)

        self.slap_button = Button(Point(750, 550), Point(1050, 700), "SLAP")
        self.slap_button.body.setFill("red")
        self.slap_button.label.setSize(24)
        self.slap_button.draw(self.win)

    def check_buttons(self):
        while True:
            click1 = self.win.getMouse()
            if self.reveal_button.inside(click1):
                card = RandomCard()
                card_file, value = card.generate()
                DisplayCard(card_file, self.win)
                # additional code to handle the reveal action
            if self.slap_button.inside(click1):
                # additional code to handle the slap action
                pass


if __name__ == "__main__":
    main = Main()
    main.check_buttons()
