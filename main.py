from graphics import *
import typing
import random
import time
import sys


class Button:
    def __init__(self, p1: Point, p2: Point, label: str):
        self.body = Rectangle(p1, p2)
        self.label = Text(Point((p1.getX() + p2.getX()) / 2, (p1.getY() + p2.getY()) / 2), label)
        self.enabled = True

    def draw(self, window: GraphWin):
        self.body.draw(window)
        self.label.draw(window)
        window.items.append(self)

    def undraw(self, window: GraphWin):
        self.body.undraw()
        self.label.undraw()
        window.items.remove(self)

    def bind_click(self, win: GraphWin, fn: typing.Callable):
        win.tag_bind(self.body.id, "<Button-1>", fn)
        win.tag_bind(self.label.id, "<Button-1>", fn)

    def unbind_click(self, win: GraphWin):
        win.tag_unbind(self.body.id, "<Button-1>")
        win.tag_bind(self.label.id, "<Button-1>")

    def inside(self, click: Point) -> bool:
        p1x = min(self.body.getP1().getX(), self.body.getP2().getX())
        p1y = min(self.body.getP1().getY(), self.body.getP2().getY())
        p2x = max(self.body.getP1().getX(), self.body.getP2().getX())
        p2y = max(self.body.getP1().getY(), self.body.getP2().getY())
        return p1x < click.getX() < p2x and p1y < click.getY() < p2y


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


class BlackjackGame:
    """A class representing a game of blackjack."""

    def __init__(self):
        """Initialize a new game of blackjack."""
        self.deck = None
        self.dealer_hand = None
        self.player_hand = None
        self.player_win = False
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

    @staticmethod
    def get_card_image_file(value: int, suit: int) -> str:
        """Return the file name of the image for the given card."""
        values = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
        suits = ["diamonds", "clubs", "hearts", "spades"]
        return f"./cards/{values[value - 1]}_of_{suits[suit - 1]}.png"

    def close_win(self, event=None):
        self.win.close()
        sys.exit()

    def start_new_game(self, event=None):
        """Start a new game of blackjack."""
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

        self.dealer_card_images.append(Image(Point(750, 200), "./images/card_back.png"))
        self.dealer_card_images.append(Image(Point(850, 200),
                                             self.get_card_image_file(self.dealer_hand.cards[1].value,
                                                                      self.dealer_hand.cards[1].get_suit_int())))

        self.dealer_card_images[0].draw(self.win)
        self.dealer_card_images[1].draw(self.win)

    def hit(self, event=None):
        """Draw a new card for the player."""
        if not self.btn_hit.enabled:
            return

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
            """Show lose screen and lose money"""

        elif self.player_hand.get_sum_bj() == 21:
            self.win = True
            self.btn_hit.enabled = False
            """Add end game or win stuff here later"""

    def stand(self, event=None):
        """End the player's turn and start the dealer's turn."""
        self.btn_hit.enabled = False
        self.dealer_turn()

    def dealer_turn(self):

        self.dealer_card_images[0].undraw()
        self.dealer_card_images[0] = Image(Point(750, 200),
                                           self.get_card_image_file(self.dealer_hand.cards[0].value,
                                                                    self.dealer_hand.cards[0].get_suit_int()))
        self.dealer_card_images[0].draw(self.win)
        self.win.tag_raise(self.dealer_card_images[1].id)
        self.lbl_dealer_score.setText(f"Dealer Score: {self.dealer_hand.get_sum_bj()}")

        while self.dealer_hand.get_sum_bj() < 17:
            time.sleep(0.4)

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

        if self.player_hand.get_sum_bj() > 21:
            pass
            """Add end game or lose stuff here later"""
        elif self.player_hand.get_sum_bj() > self.dealer_hand.get_sum_bj():
            self.player_win = True
            """Add end game or win stuff here later"""
        elif self.player_hand.get_sum_bj() == self.dealer_hand.get_sum_bj():
            self.player_win = True
            """Add end game or tie stuff here later"""

    def play(self):
        """Bind the event listeners to the buttons."""
        self.btn_hit.bind_click(self.win, self.hit)
        self.btn_stand.bind_click(self.win, self.stand)
        self.btn_new_game.bind_click(self.win, self.start_new_game)
        self.win.mainloop()


def main():
    """Main entry point for the program."""
    game = BlackjackGame()
    game.start_new_game()
    game.play()


main()
