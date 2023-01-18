import random


class Card:

    # 1 = Diamonds, 2 = Clubs, 3 = Hearts, 4 = Spades
    # 1 = Ace, 11 = Jack, 12 = Queen, 13 = King
    # Creating the card requires two arguments, the suit and the value
    def __init__(self, suit: int, value: int):
        # initialize the card with the given suit and value
        suits = ["Diamonds", "Clubs", "Hearts", "Spades"]
        self.suit = suits[suit - 1]
        self.value = value

    # Return the suit of the card as a string (Diamonds, Clubs, Hearts, Spades)
    def get_suit_str(self) -> str:
        return self.suit

    # Return the value of the suit as an int (1 = Diamonds, 2 = Clubs, 3 = Hearts, 4 = Spades)
    def get_suit_int(self) -> int:
        return ["Diamonds", "Clubs", "Hearts", "Spades"].index(self.suit) + 1

    # Return the value of the card as an int (1 = Ace, 11 = Jack, 12 = Queen, 13 = King)
    def get_value(self) -> int:
        return self.value

    # Get the name of the card (e.g. Ace of Diamond, 2 of Clubs)
    def get_name(self) -> str:
        # For special cards like ace or kings, return the name of the card instead of the number
        value = str()
        if self.value > 10 or self.value == 1:
            if self.value == 1:
                value = "Ace"
            if self.value == 11:
                value = "Jack"
            elif self.value == 12:
                value = "Queen"
            elif self.value == 13:
                value = "King"
        # If it is a regular card will just return the number
        else:
            value = self.value

        # Return the name of the card formatted as "Value of Suit"
        return f"{value} of {self.suit}"


class Deck:

    # When creating a deck object, will add all 52 cards to the deck
    def __init__(self):
        # Create a list to store the cards in the deck
        self.cards = []
        # Add all 52 cards to the deck using a nested for loop
        for i in range(13):
            for j in range(4):
                # Add a card object to the deck
                self.cards.append(Card(j + 1, i + 1))

    # Shuffle the deck of cards using the random library
    def shuffle(self) -> None:
        random.shuffle(self.cards)

    # Removes the top card of the deck and returns it
    def draw(self) -> Card:
        return self.cards.pop()

    # Removes all the cards in the deck and re-adds the 52 original cards
    def reset(self):
        """Reset the deck of cards."""
        self.cards.clear()
        for i in range(13):
            for j in range(4):
                self.cards.append(Card(j + 1, i + 1))


# A class representing the hand of a single player
class Hand:
    # Initialise a new empty hand
    def __init__(self):
        self.cards = []

    # Adds a card to the hand
    def add_card(self, card: Card):
        if type(card) is not Card:
            raise TypeError("The card must be a Card object")
        self.cards.append(card)

    # Returns a list of the cards in the list
    def get_cards(self) -> list:
        return self.cards

    # Return the number of the cards of the hand
    def size(self) -> int:
        return len(self.cards)

    # Return the sum of the values of the hand, specifically for blackjack
    def get_sum_bj(self) -> int:
        # Aces will automatically be counted as 11, but will be changed to 1 if the sum is over 21

        # Variable to store the sum of the hand the number of aces that are currently being counted as 11
        total = 0
        aces11 = 0

        # Loop through all the cards in the hand
        for card in self.cards:
            # Count all royal cards as 10
            if card.get_value() > 10:
                total += 10
            # if it is an ace, count it as 11, and increase the number of aces that are being counted as 11
            elif card.get_value() == 1:
                total += 11
                aces11 += 1
            # Could all regular playing cards as their regular value
            else:
                total += card.get_value()

        # If the sum is over 21, and there are aces that are being counted as 11,
        # change them to 1 until the sum is under 21
        while total > 21 and aces11 > 0:
            total -= 10
            aces11 -= 1

        # Return the sum of the hand
        return total

    # Reset the hand by removing all the cards
    def reset(self):
        self.cards.clear()
