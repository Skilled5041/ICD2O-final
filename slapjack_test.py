from graphics import *
from graphics_elements import Button
import random


class SlapjackGame:
    def __init__(self):
        self.win = GraphWin("Slapjack", 1200, 800)
        self.deck = Deck()
        self.deck.shuffle()
        self.hand = Hand()
        self.top_card = None
        self.slap_button = Button(Point(1050, 750), Point(1100, 775), "SLAP")
        self.slap_button.body.setFill("red")
        self.slap_button.draw(self.win)
        self.card_image = None

        # # create new button
        self.reveal_button = Button(Point(1000, 750), Point(1050, 775), "REVEAL")
        self.reveal_button.body.setFill("green")
        self.reveal_button.draw(self.win)

    @staticmethod
    def get_card_image_file(value: int, suit: int) -> str:
        """Return the file name of the image for the given card."""
        values = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
        suits = ["diamonds", "clubs", "hearts", "spades"]
        return f"./cards/{values[value - 1]}_of_{suits[suit - 1]}.png"

    def run(self):
        self.slap_button.bind_click(self.win, self.slap)
        self.slap_button.bind_click(self.win, self.reveal_card)

    def slap(self):
        self.top_card = self.deck.draw()
        self.hand.add_card(self.top_card)
        self.card_image = Image(Point(600, 400), "./images/card_back.png")
        self.card_image.draw(self.win)
        self.check_slap()

    def check_slap(self):
        """checks if the player has won or lost"""
        pass

    def reveal_card(self):
        """ reveal the top card """
        self.card_image.undraw()
        card_image_file = self.get_card_image_file(self.top_card.get_value(), self.top_card.get_suit_int())
        self.card_image = Image(Point(600, 400), card_image_file)
        self.card_image.draw(self.win)


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


slapjack = SlapjackGame()
slapjack.run()
slapjack.win.mainloop()
