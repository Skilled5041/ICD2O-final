from graphics import *
import typing
import random


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

    def unbind_click(self, win: GraphWin):
        win.tag_unbind(self.body.id, "<Button-1>")

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

    def __init__(self, cards: list):
        """Initialize a new hand with the given list of cards."""
        self.cards = cards

    def add_card(self, card: Card):
        """Add a card to the hand."""
        self.cards.append(card)

    """May change this later"""

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


class BlackjackGame:
    """A class representing a game of blackjack."""

    def __init__(self):
        """Initialize a new game of blackjack."""
        self.deck = None
        self.dealer_hand = None
        self.player_hand = None
        self.win = GraphWin("Blackjack", 1200, 800)

        self.bg = Image(Point(600, 400), "./images/bj_bg.png")
        self.bg.draw(self.win)

        self.btn_hit = Button(Point(50, 500), Point(150, 550), "Hit")
        self.btn_hit.body.setFill("white")
        self.btn_hit.draw(self.win)

        self.btn_stand = Button(Point(200, 500), Point(300, 550), "Stand")
        self.btn_stand.body.setFill("white")
        self.btn_stand.draw(self.win)

        self.btn_new_game = Button(Point(350, 500), Point(450, 550), "New Game")
        self.btn_new_game.body.setFill("white")
        self.btn_new_game.draw(self.win)

        self.card_slots = []
        for i in range(5):
            self.card_slots.append(Rectangle(Point(50 + i * 100, 50), Point(150 + i * 100, 250)))
            self.card_slots[i].draw(self.win)

        self.card_images = []
        for i in range(5):
            self.card_images.append(Image(Point(100 + i * 100, 150), "./images/card_back.png"))
            self.card_images[i].draw(self.win)

        self.lbl_player_score = Text(Point(100, 300), "Player Score: 0")
        self.lbl_player_score.setTextColor("white")
        self.lbl_player_score.draw(self.win)

        self.lbl_dealer_score = Text(Point(700, 300), "Dealer Score: 0")
        self.lbl_dealer_score.setTextColor("white")
        self.lbl_dealer_score.draw(self.win)

    def start_new_game(self, event=None):
        """Start a new game of blackjack."""
        self.player_hand = Hand([])
        self.dealer_hand = Hand([])

        self.deck = Deck()
        self.deck.shuffle()

        self.player_hand.add_card(self.deck.draw())
        self.player_hand.add_card(self.deck.draw())

        self.dealer_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())

        self.lbl_player_score.setText(f"Player Score: {self.player_hand.get_sum_bj()}")

        self.card_images[0].undraw()
        self.card_images[1].undraw()

        self.card_images[2] = Image(Point(100, 150), self.get_card_image_file(self.player_hand.cards[0].get_value(),
                                                                              self.player_hand.cards[0].get_suit_int()))
        self.card_images[2].draw(self.win)

    @staticmethod
    def get_card_image_file(value: "int 1 - 13", suit: "int 1 - 4") -> str:
        """Return the file name of the image for the given card."""
        values = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
        suits = ["diamonds", "clubs", "hearts", "spades"]
        return f"./cards/{values[value - 1]}_of_{suits[suit - 1]}.png"

    def hit(self, event=None):
        """Draw a new card for the player."""
        self.player_hand.add_card(self.deck.draw())

        self.lbl_player_score.setText(f"Player Score: {self.player_hand.get_sum_bj()}")

        # self.card_images[self.player_hand.get_value() - 1].setImage(
        #     self.get_card_image_file(self.player_hand.cards[-1]))

    def stand(self, event=None):
        """End the player's turn and start the dealer's turn."""
        # have to add code to implement the dealer's turn
        pass

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
