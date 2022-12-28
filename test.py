from graphics import *
import random


class Card:
    """A class representing a single playing card."""
    """1 = Diamonds, 2 = Clubs, 3 = Hearts, 4 = Spades"""
    """1 = Ace, 11 = Jack, 12 = Queen, 13 = King"""

    def __init__(self, suit: "int 1 - 4", value: "int 1 - 13"):
        """Initialize a new Card with the given suit and value."""
        suits = ["Diamonds", "Clubs", "Hearts", "Spades"]
        self.suit = suits[suit - 1]
        self.value = value

    def get_suit(self) -> str:
        """Return the suit of the card."""
        return self.suit

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

    def __init__(self, cards: list):
        """Initialize a new hand with the given list of cards."""
        self.cards = cards

    def add_card(self, card):
        """Add a card to the hand."""
        self.cards.append(card)

    def get_sum_bj(self) -> int:
        """Return the sum of the values of the cards in the hand, specifically for blackjack."""
        total = 0
        aces11 = 0
        for card in self.cards:
            if card.get_value() > 10:
                """Add 10 if the card is a jack, queen, or king."""
                total += 10
                if total > 21 and aces11 > 0:
                    """If the total is over 21 and there are aces in the hand that are worth 11,
                     subtract 10 from the total to make the ace worth 1."""
                    total -= 10
                    aces11 -= 1
            elif card.get_value() == 1:
                """If it is an ace add 11 or 1 depending if the total will go over 21."""
                total += 11 if total + 11 <= 21 else 1
                aces11 += 1 if total + 11 <= 21 else 0
            else:
                total += card.get_value()
                if total > 21 and aces11 > 0:
                    """If the total is over 21 and there are aces in the hand that are worth 11,
                    subtract 10 from the total to make the ace worth 1."""
                    total -= 10
                    aces11 -= 1

        return total


win = GraphWin("Blackjack", 600, 600)


c = Image(Point(300, 300), "./cards/king_of_diamonds.png")
c.draw(win)

win.getMouse()
win.close()
