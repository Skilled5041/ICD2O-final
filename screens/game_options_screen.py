# Used for unfinished feature of allowing user to choose number of players and bots

from graphics import *
from graphics_extras import Button


class GameOptionsScreen:
    def __init__(self, window):
        self.player_count = 1

        self.player_count_text = Text(Point(313, 350), "Player Count")
        self.player_count_text.setSize(24)
        self.player_count_text.draw(window)

        self.player_count_num_box = Rectangle(Point(280, 420), Point(340, 480))
        self.player_count_num_box .setFill("white")
        self.player_count_num_box.draw(window)

        self.player_count_num = Text(Point(310, 450), self.player_count)
        self.player_count_num.setSize(24)
        self.player_count_num.draw(window)

        self.remove_player_btn = Button(Point(220, 420), Point(280, 480), "-")
        self.remove_player_btn.enabled = False
        self.remove_player_btn.label.setSize(24)
        self.remove_player_btn.body.setFill("grey")
        self.remove_player_btn.draw(window)

        self.add_player_btn = Button(Point(340, 420), Point(400, 480), "+")
        self.add_player_btn.label.setSize(24)
        self.add_player_btn.body.setFill("white")
        self.add_player_btn.draw(window)

        self.bot_count = 0

        self.bot_count_text = Text(Point(887, 350), "Bot Count")
        self.bot_count_text.setSize(24)
        self.bot_count_text.draw(window)

        self.bot_count_num_box = Rectangle(Point(854, 420), Point(914, 480))
        self.bot_count_num_box.setFill("white")
        self.bot_count_num_box.draw(window)

        self.bot_count_num = Text(Point(884, 450), self.bot_count)
        self.bot_count_num.setSize(24)
        self.bot_count_num.draw(window)

        self.remove_bot_btn = Button(Point(794, 420), Point(854, 480), "-")
        self.remove_bot_btn.enabled = False
        self.remove_bot_btn.label.setSize(24)
        self.remove_bot_btn.body.setFill("grey")
        self.remove_bot_btn.draw(window)

        self.add_bot_btn = Button(Point(914, 420), Point(974, 480), "+")
        self.add_bot_btn.label.setSize(24)
        self.add_bot_btn.body.setFill("white")
        self.add_bot_btn.draw(window)

        self.add_player_btn.bind_click(window, self.add_player)
        self.remove_player_btn.bind_click(window, self.remove_player)

        self.add_bot_btn.bind_click(window, self.add_bot)
        self.remove_bot_btn.bind_click(window, self.remove_bot)

    def add_player(self, event=None):
        if self.player_count + self.bot_count < 4:
            self.player_count += 1
            self.player_count_num.setText(self.player_count)
            self.remove_player_btn.enabled = True
            self.remove_player_btn.body.setFill("white")
            if self.player_count + self.bot_count == 4:
                self.add_player_btn.enabled = False
                self.add_player_btn.body.setFill("grey")
                self.add_bot_btn.enabled = False
                self.add_bot_btn.body.setFill("grey")

    def remove_player(self, event=None):
        if self.player_count > 1:
            self.player_count -= 1
            self.player_count_num.setText(self.player_count)
            self.add_player_btn.enabled = True
            self.add_player_btn.body.setFill("white")
            self.add_bot_btn.enabled = True
            self.add_bot_btn.body.setFill("white")
            if self.player_count == 1:
                self.remove_player_btn.enabled = False
                self.remove_player_btn.body.setFill("grey")

    def add_bot(self, event=None):
        if self.player_count + self.bot_count < 4:
            self.bot_count += 1
            self.bot_count_num.setText(self.bot_count)
            self.remove_bot_btn.enabled = True
            self.remove_bot_btn.body.setFill("white")
            if self.player_count + self.bot_count == 4:
                self.add_player_btn.enabled = False
                self.add_player_btn.body.setFill("grey")
                self.add_bot_btn.enabled = False
                self.add_bot_btn.body.setFill("grey")

    def remove_bot(self, event=None):
        if self.bot_count > 0:
            self.bot_count -= 1
            self.bot_count_num.setText(self.bot_count)
            self.add_player_btn.enabled = True
            self.add_player_btn.body.setFill("white")
            self.add_bot_btn.enabled = True
            self.add_bot_btn.body.setFill("white")
            if self.bot_count == 0:
                self.remove_bot_btn.enabled = False
                self.remove_bot_btn.body.setFill("grey")


win = GraphWin("Game Options", 1200, 800)
GameOptionsScreen(win)
win.mainloop()
