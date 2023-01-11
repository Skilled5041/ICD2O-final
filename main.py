from graphics import *
from graphics_elements import Button
from win_and_lose_screens import win_window, lose_window, tie_window
from audioplayer import AudioPlayer
import random
import sys
import time


def undraw_all(window):
    for i in range(len(window.items)):
        if type(window.items[0]) is Button:
            window.items[0].undraw(window)
        elif type(window.items[0]) is not Button:
            window.items[0].undraw()


class Card:
    """A class representing a single playing card."""
    """1 = Diamonds, 2 = Clubs, 3 = Hearts, 4 = Spades"""
    """1 = Ace, 11 = Jack, 12 = Queen, 13 = King"""

    def __init__(self, suit: int, value: int):
        """Initialize a new Card with the given suit and value."""
        suits = ["Diamonds", "Clubs", "Hearts", "Spades"]
        self.suit = suits[suit - 1]
        self.value = value

    def get_suit_str(self) -> str:
        """Return the suit of the card."""
        return self.suit

    def get_suit_int(self) -> int:
        # Get the suit of the card as an integer (1 = Diamonds, 2 = Clubs, 3 = Hearts, 4 = Spades)
        return ["Diamonds", "Clubs", "Hearts", "Spades"].index(self.suit) + 1

    def get_value(self) -> int:
        """Return the value of the card."""
        return self.value

    def get_name(self) -> str:
        """Return the name of the card, such as 'Ace of Spades'."""
        if self.value > 10 or self.value == 1:
            if self.value == 1:
                value = "Ace"
            if self.value == 11:
                value = "Jack"
            elif self.value == 12:
                value = "Queen"
            elif self.value == 13:
                value = "King"

        else:
            value = self.value

        return f"{value} of {self.suit}"


class Deck:
    """A class representing a deck of playing cards."""

    def __init__(self):
        """Initialize a new deck of 52 cards."""
        self.cards = []
        for i in range(13):
            for j in range(4):
                self.cards.append(Card(j + 1, i + 1))

    def shuffle(self):
        """Shuffle the deck of cards."""
        random.shuffle(self.cards)

    def draw(self) -> Card:
        """Draw the top card from the deck and return it."""
        return self.cards.pop()

    def reset(self):
        """Reset the deck of cards."""
        self.cards.clear()
        for i in range(13):
            for j in range(4):
                self.cards.append(Card(j + 1, i + 1))


class Hand:
    """A class representing a player's hand in a card game."""

    def __init__(self):
        """Initialize a new hand with the given list of cards."""
        self.cards = []

    def add_card(self, card: Card):
        """Add a card to the hand."""
        self.cards.append(card)

    def get_cards(self) -> list:
        """Return the cards in the hand."""
        return self.cards

    def size(self) -> int:
        """Return the number of cards in the hand."""
        return len(self.cards)

    """May change this later"""

    def get_sum_bj(self) -> int:
        """Return the sum of the values of the cards in the hand, specifically for blackjack."""
        total = 0
        aces11 = 0
        for card in self.cards:
            if card.get_value() > 10:
                """Add 10 if the card is a jack, queen, or king."""
                total += 10
            elif card.get_value() == 1:
                total += 11
                aces11 += 1
            else:
                total += card.get_value()

        while total > 21 and aces11 > 0:
            total -= 10
            aces11 -= 1

        return total

    def reset(self):
        """Reset the hand."""
        self.cards.clear()


class BlackjackGame:
    """A class representing a game of blackjack."""

    def __init__(self):
        """Initialize a new game of blackjack."""
        self.current_screen = "game"
        self.deck = None
        self.dealer_hand = None
        self.player_hand = None
        self.player_win = False
        self.player_lose = False
        self.player_bust = False

        self.win = GraphWin("Blackjack", 1200, 800)

        self.bg = Image(Point(600, 400), "./images/bj_bg.png")
        self.bg.draw(self.win)

        self.close_btn = Button(Point(0, 0), Point(30, 30), "X")
        self.close_btn.body.setFill("red")
        self.close_btn.body.setOutline("red")
        self.close_btn.draw(self.win)
        self.close_btn.bind_click(self.win, self.close_win)

        self.btn_hit = Button(Point(200, 620), Point(400, 700), "Hit")
        self.btn_hit.body.setFill("white")
        self.btn_hit.label.setSize(24)
        self.btn_hit.draw(self.win)

        self.btn_stand = Button(Point(500, 620), Point(700, 700), "Stand")
        self.btn_stand.body.setFill("white")
        self.btn_stand.label.setSize(24)
        self.btn_stand.draw(self.win)

        self.btn_new_game = Button(Point(800, 620), Point(1000, 700), "New Game")
        self.btn_new_game.body.setFill("white")
        self.btn_new_game.label.setSize(24)
        self.btn_new_game.draw(self.win)

        self.player_card_images = []
        self.dealer_card_images = []

        self.lbl_player_score = Text(Point(200, 350), "Player Score: 0")
        self.lbl_player_score.setTextColor("white")
        self.lbl_player_score.draw(self.win)

        self.lbl_dealer_score = Text(Point(800, 350), "Dealer Score: ???")
        self.lbl_dealer_score.setTextColor("white")
        self.lbl_dealer_score.draw(self.win)

        self.result_text = Text(Point(600, 650), "")
        self.result_text.setSize(36)

        self.dealer_playing = False

        self.hitsound = AudioPlayer("./sounds/hit_sfx.mp3")
        self.standsound = AudioPlayer("./sounds/stand_sfx.mp3")

    @staticmethod
    def get_card_image_file(value: int, suit: int) -> str:
        """Return the file name of the image for the given card."""
        values = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
        suits = ["diamonds", "clubs", "hearts", "spades"]
        return f"./cards/{values[value - 1]}_of_{suits[suit - 1]}.png"

    @staticmethod
    def close_win(event=None):
        sys.exit()

    def start_new_game(self, event=None):
        """Start a new game of blackjack."""

        # TODO: Make it reset the game properly and start a new game

        self.player_hand = Hand()
        self.dealer_hand = Hand()

        self.deck = Deck()
        self.deck.shuffle()

        self.player_hand.add_card(self.deck.draw())
        self.player_hand.add_card(self.deck.draw())

        self.dealer_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())

        self.lbl_player_score.setText(f"Player Score: {self.player_hand.get_sum_bj()}")
        self.lbl_dealer_score.setText(f"Dealer Score: ???")

        self.player_card_images.append(Image(Point(150, 200),
                                             self.get_card_image_file(self.player_hand.cards[0].value,
                                                                      self.player_hand.cards[0].get_suit_int())))
        self.player_card_images.append(Image(Point(250, 200),
                                             self.get_card_image_file(self.player_hand.cards[1].value,
                                                                      self.player_hand.cards[1].get_suit_int())))

        self.player_card_images[0].draw(self.win)
        self.player_card_images[1].draw(self.win)

        self.dealer_card_images.append(Image(Point(750, 200),
                                             self.get_card_image_file(self.dealer_hand.cards[1].value,
                                                                      self.dealer_hand.cards[1].get_suit_int())))
        self.dealer_card_images.append(Image(Point(850, 200), "./images/card_back.png"))

        self.dealer_card_images[0].draw(self.win)
        self.dealer_card_images[1].draw(self.win)

        if self.player_hand.get_sum_bj() == 21:
            self.player_win = True
            self.btn_hit.enabled = False
            self.result_text.setText("You got 21! You won!")
            self.on_player_win()

    def hit(self, event=None):

        """Draw a new card for the player."""
        if not self.btn_hit.enabled:
            return

        self.hitsound.play(loop=False, block=False)

        if self.player_hand.size() % 4 == 0:
            self.lbl_player_score.move(0, 80)

        self.player_hand.add_card(self.deck.draw())
        self.lbl_player_score.setText(f"Player Score: {self.player_hand.get_sum_bj()}")

        # make it so there are max 4 card by row, and the next row moves down by 60 pixels
        self.player_card_images.append(
            Image(Point(150 + (len(self.player_card_images) % 4) * 100, 200 + (len(self.player_card_images) // 4) * 80),
                  self.get_card_image_file(self.player_hand.cards[-1].value,
                                           self.player_hand.cards[-1].get_suit_int())))
        self.player_card_images[-1].draw(self.win)

        if self.player_hand.get_sum_bj() > 21:
            self.player_bust = True
            self.btn_hit.enabled = False

            self.result_text.setText("You bust!")
            self.on_player_lose()

        elif self.player_hand.get_sum_bj() == 21:
            self.player_win = True
            self.btn_hit.enabled = False
            self.result_text.setText("You got 21! You Win!")
            self.on_player_win()

    def stand(self, event=None):
        """End the player's turn and start the dealer's turn."""
        if not self.btn_stand.enabled:
            return
        self.btn_hit.enabled = False
        self.btn_stand.enabled = False
        self.standsound.play(loop=False, block=False)

        self.dealer_turn()

    def dealer_turn(self):

        if self.dealer_playing:
            return

        self.dealer_playing = True
        self.dealer_card_images[1].undraw()
        self.dealer_card_images[1] = Image(Point(850, 200),
                                           self.get_card_image_file(self.dealer_hand.cards[0].value,
                                                                    self.dealer_hand.cards[0].get_suit_int()))
        self.dealer_card_images[1].draw(self.win)
        self.win.tag_raise(self.dealer_card_images[1].id)
        self.lbl_dealer_score.setText(f"Dealer Score: {self.dealer_hand.get_sum_bj()}")

        while self.dealer_hand.get_sum_bj() < 17:
            time.sleep(0.8)

            if self.dealer_hand.size() % 4 == 0:
                self.lbl_dealer_score.move(0, 80)

            self.dealer_hand.add_card(self.deck.draw())
            self.dealer_card_images.append(
                Image(
                    Point(750 + (len(self.dealer_card_images) % 4) * 100,
                          200 + (len(self.dealer_card_images) // 4) * 80),
                    self.get_card_image_file(self.dealer_hand.cards[-1].value,
                                             self.dealer_hand.cards[-1].get_suit_int())))

            self.dealer_card_images[-1].draw(self.win)
            self.lbl_dealer_score.setText(f"Dealer Score: {self.dealer_hand.get_sum_bj()}")

        if self.dealer_hand.get_sum_bj() > 21:
            self.player_win = True
            self.result_text.setText("Dealer Busts! You Win!")
            self.on_player_win()
        elif self.player_hand.get_sum_bj() > self.dealer_hand.get_sum_bj():
            self.player_win = True
            self.result_text.setText("Your hand is higher! You Win!")
            self.on_player_win()
        elif self.player_hand.get_sum_bj() < self.dealer_hand.get_sum_bj():
            self.player_lose = True

            self.result_text.setText("Dealer's hand is higher! You Lose!")
            self.on_player_lose()

        elif self.player_hand.get_sum_bj() == self.dealer_hand.get_sum_bj():
            self.player_win = True
            self.result_text.setText("It's a tie!")
            self.on_player_tie()

    def play(self):
        """Bind the event listeners to the buttons."""
        if self.current_screen != "game":
            return

        self.btn_hit.bind_click(self.win, self.hit)
        self.btn_stand.bind_click(self.win, self.stand)
        self.btn_new_game.bind_click(self.win, self.start_new_game)

    def on_player_win(self):
        self.btn_hit.enabled = False
        self.btn_stand.enabled = False
        time.sleep(1.5)
        self.win.unbind_all("<Button-1>")
        undraw_all(self.win)
        win_window(self.win, self.player_hand.get_sum_bj(), self.dealer_hand.get_sum_bj())
        self.result_text.draw(self.win)
        self.close_btn.draw(self.win)
        self.close_btn.bind_click(self.win, self.close_win)
        self.current_screen = "win"

    def on_player_lose(self):
        self.btn_hit.enabled = False
        self.btn_stand.enabled = False
        time.sleep(1.5)
        self.win.unbind_all("<Button-1>")
        undraw_all(self.win)
        lose_window(self.win, self.player_hand.get_sum_bj(), self.dealer_hand.get_sum_bj())
        self.result_text.draw(self.win)
        self.close_btn.draw(self.win)
        self.close_btn.bind_click(self.win, self.close_win)
        self.current_screen = "lose"

    def on_player_tie(self):
        self.btn_hit.enabled = False
        self.btn_stand.enabled = False
        time.sleep(1.5)
        self.win.unbind_all("<Button-1>")
        undraw_all(self.win)
        tie_window(self.win, self.player_hand.get_sum_bj(), self.dealer_hand.get_sum_bj())
        self.result_text.draw(self.win)
        self.close_btn.draw(self.win)
        self.close_btn.bind_click(self.win, self.close_win)
        self.current_screen = "tie"


def main():
    """Main entry point for the program."""
    game = BlackjackGame()
    game.start_new_game()
    game.play()
    game.win.mainloop()


main()
