from graphics import *
from graphics_elements import Button
from win_and_lose_screens import win_window, lose_window, tie_window
from audioplayer import AudioPlayer
import random
import sys
import time
import edit_stats


# Function to undraw everything in the window
def undraw_all(window):
	# Loop through all the items in the window that are currently drawn
	for i in range(len(window.items)):
		# Depending on the type of item, undraw it differently (the button I made requires an argument)
		if type(window.items[0]) is Button:
			window.items[0].undraw(window)
		elif type(window.items[0]) is not Button:
			window.items[0].undraw()


# Class for representing a singe playing card
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


# A class representing a single deck of playing cards
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
	def shuffle(self):
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


# Class representing a game of blackjack
class BlackjackGame:

	def __init__(self, win: GraphWin):
		"""Initialize a new game of blackjack."""

		# TODO Should probably move this somewhere else
		self.current_screen = "game"

		# Initialise the deck, the player's hand, and the dealer's hand
		self.deck = None
		self.dealer_hand = None
		self.player_hand = None

		# Variable to track whether the hit function is currently being executed to prevent bugs
		self.hitting = False

		# TODO Might not need this
		# Variable to track whether the dealer is currently playing
		self.dealer_playing = False

		# TODO Remove this maybe, idk if they're needed
		self.player_win = False
		self.player_lose = False
		self.player_bust = False

		# TODO should probably create the window somewhere else
		self.win = win

		# Create the background
		self.bg = Image(Point(600, 400), "./images/bj_bg.png")

		# Create the close button
		self.close_btn = Button(Point(0, 0), Point(30, 30), "X")
		self.close_btn.body.setFill("red")
		self.close_btn.body.setOutline("red")

		# Create the hit button
		self.btn_hit = Button(Point(200, 620), Point(400, 700), "Hit")
		self.btn_hit.body.setFill("white")
		self.btn_hit.label.setSize(24)

		# Create the stand button
		self.btn_stand = Button(Point(500, 620), Point(700, 700), "Stand")
		self.btn_stand.body.setFill("white")
		self.btn_stand.label.setSize(24)

		# Create the new game button
		self.btn_new_game = Button(Point(800, 620), Point(1000, 700), "New Game")
		self.btn_new_game.body.setFill("white")
		self.btn_new_game.label.setSize(24)

		# List to store the images of the cards in the player's hand and the dealers hand
		self.player_card_images = []
		self.dealer_card_images = []

		# Labels to display the sum of the player's hand and the dealer's hand
		self.lbl_player_score = Text(Point(200, 350), "Player Score: 0")
		self.lbl_player_score.setTextColor("white")

		# The sum of the dealer's hand is hidden in the beginning
		self.lbl_dealer_score = Text(Point(800, 350), "Dealer Score: ???")
		self.lbl_dealer_score.setTextColor("white")

		# TODO Should move this to other screens
		self.result_text = Text(Point(600, 650), "")
		self.result_text.setSize(36)

		# TODO Could put this in a different file
		# Store the sounds in variables
		self.hitsound = AudioPlayer("./sounds/hit_sfx.mp3")
		self.standsound = AudioPlayer("./sounds/stand_sfx.mp3")

	# TODO Should probably put this outside of the class
	# Function to get the name of an image file for a card
	@staticmethod
	def get_card_image_file(value: int, suit: int) -> str:
		# Return the file name of the card image
		values = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
		suits = ["diamonds", "clubs", "hearts", "spades"]
		return f"./cards/{values[value - 1]}_of_{suits[suit - 1]}.png"

	# TODO Should probably put this outside of the class and where the window is being created
	# Function the close the window and stop the program
	def close_win(self, event=None):
		# Animation to make the window transparent
		for i in range(100):
			# Set the transparency of the window
			self.win.master.attributes("-alpha", 1 - i / 100)
			time.sleep(0.01)
		# Exit the program
		sys.exit()

	# Function to start a new game of blackjack
	def start_new_game(self, event=None):

		# TODO Should probably only undraw certain things
		undraw_all(self.win)

		self.bg.draw(self.win)
		self.close_btn.draw(self.win)
		self.btn_hit.draw(self.win)
		self.btn_stand.draw(self.win)
		self.btn_new_game.draw(self.win)
		self.lbl_player_score.draw(self.win)
		self.lbl_dealer_score.draw(self.win)
		self.player_card_images.clear()
		self.dealer_card_images.clear()

		self.btn_hit.enabled = False

		self.play()

		# TODO: Make it reset the game properly and start a new game

		# Create a hand for the player and dealer
		self.player_hand = Hand()
		self.dealer_hand = Hand()

		# Create the deck and shuffle it
		self.deck = Deck()
		self.deck.shuffle()

		# Deal two cards to the player and the dealer
		self.player_hand.add_card(self.deck.draw())
		self.player_hand.add_card(self.deck.draw())

		self.dealer_hand.add_card(self.deck.draw())
		self.dealer_hand.add_card(self.deck.draw())

		# Reset the text of the score labels
		self.lbl_player_score.setText(f"Player Score: {self.player_hand.get_sum_bj()}")
		self.lbl_dealer_score.setText(f"Dealer Score: ???")

		# Add the images of the cards to the list of card images
		self.player_card_images.append(Image(Point(150, 200),
											 self.get_card_image_file(self.player_hand.cards[0].value,
																	  self.player_hand.cards[0].get_suit_int())))
		self.player_card_images.append(Image(Point(250, 200),
											 self.get_card_image_file(self.player_hand.cards[1].value,
																	  self.player_hand.cards[1].get_suit_int())))

		# Draw the two cards in the player's hand
		self.player_card_images[0].draw(self.win)
		self.player_card_images[1].draw(self.win)

		# Add the images of the cards to the list of card images
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
		if (not self.btn_hit.enabled) or self.hitting:
			return

		self.hitting = True

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

		elif self.player_hand.get_sum_bj() == 21 and self.dealer_hand.get_sum_bj() != 21:
			self.player_win = True
			self.btn_hit.enabled = False
			self.result_text.setText("You got 21! You Win!")
			self.on_player_win()
		elif self.player_hand.get_sum_bj == 21 and self.dealer_hand.get_sum_bj == 21:
			self.result_text.setText("You both got 21! It's a tie!")
			self.on_player_tie()

		self.hitting = False

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

		self.close_btn.bind_click(self.win, self.close_win)
		self.btn_hit.bind_click(self.win, self.hit)
		self.btn_stand.bind_click(self.win, self.stand)
		self.btn_new_game.bind_click(self.win, self.start_new_game)

	def on_player_win(self):
		edit_stats.add_win()
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
		edit_stats.add_loss()
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
		edit_stats.add_tie()
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
	win = GraphWin("Blackjack", 1200, 800)

	game = BlackjackGame(win)
	game.start_new_game()
	win.mainloop()


main()
