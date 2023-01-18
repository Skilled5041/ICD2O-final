from cards import *
from graphics import *
from graphics_elements import Button
from game import Game
from win_and_lose_screens import WinScreen, lose_window, tie_window
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


# Class representing a game of blackjack
class BlackjackGame:

    def __init__(self):
        # Initialise the blackjack screen
        # Initialise the deck, the player's hand, and the dealer's hand
        self.deck = None
        self.dealer_hand = None
        self.player_hand = None

        # Variable to track whether the hit function is currently being executed to prevent bugs
        self.hitting = False

        # Tracks how much the score labels have moved, so when a new game is started, the labels can be moved back
        self.player_score_moved_amount = 0
        self.dealer_score_moved_amount = 0

        # Create the background
        self.bg = Image(Point(600, 400), "./images/bj_bg.png")

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

    def draw_screen(self):

        self.bg.draw(Game.window)
        Game.close_btn.draw(Game.window)
        self.btn_hit.draw(Game.window)
        self.btn_stand.draw(Game.window)
        self.btn_new_game.draw(Game.window)
        self.lbl_player_score.draw(Game.window)
        self.lbl_dealer_score.draw(Game.window)

    # Function to start a new game of blackjack
    def start_new_game(self, event=None):

        for image in self.player_card_images:
            image.undraw()
        for image in self.dealer_card_images:
            image.undraw()

        self.player_card_images.clear()
        self.dealer_card_images.clear()

        self.lbl_player_score.move(0, -self.player_score_moved_amount)
        self.lbl_dealer_score.move(0, -self.dealer_score_moved_amount)

        self.player_score_moved_amount = 0
        self.dealer_score_moved_amount = 0

        self.btn_hit.enabled = True
        self.btn_stand.enabled = True
        self.hitting = False

        self.bind_button_clicks()

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
        self.player_card_images.append(Image(Point(150, 200), Game.get_card_image_file(self.player_hand.cards[0])))
        self.player_card_images.append(Image(Point(250, 200), Game.get_card_image_file(self.player_hand.cards[1])))

        # Draw the two cards in the player's hand
        self.player_card_images[0].draw(Game.window)
        self.player_card_images[1].draw(Game.window)

        # Add the images of the cards to the list of card images
        self.dealer_card_images.append(Image(Point(750, 200), Game.get_card_image_file(self.dealer_hand.cards[0])))
        self.dealer_card_images.append(Image(Point(850, 200), "./images/card_back.png"))

        self.dealer_card_images[0].draw(Game.window)
        self.dealer_card_images[1].draw(Game.window)

        if self.player_hand.get_sum_bj() == 21 and self.dealer_hand.get_sum_bj() != 21:

            self.btn_hit.enabled = False

            # Show the dealer's hidden card
            self.dealer_card_images[1].undraw()
            self.dealer_card_images[1] = Image(Point(850, 200), Game.get_card_image_file(self.dealer_hand.cards[1]))
            self.dealer_card_images[1].draw(Game.window)
            self.lbl_dealer_score.setText(f"Dealer Score: {self.dealer_hand.get_sum_bj()}")

            self.on_player_win(result_text="You got a Blackjack! You win!")

        elif self.player_hand.get_sum_bj() == 21 and self.dealer_hand.get_sum_bj() == 21:
            self.btn_hit.enabled = False

            # Show the dealer's hidden card
            self.dealer_card_images[1].undraw()
            self.dealer_card_images[1] = Image(Point(850, 200), Game.get_card_image_file(self.dealer_hand.cards[1]))
            self.dealer_card_images[1].draw(Game.window)
            self.lbl_dealer_score.setText(f"Dealer Score: {self.dealer_hand.get_sum_bj()}")

            self.result_text.setText("You both got 21! It's a tie!")
            self.on_player_tie()

        elif self.player_hand.get_sum_bj() != 21 and self.dealer_hand.get_sum_bj() == 21:

            self.btn_hit.enabled = False

            # Show the dealer's hidden card
            self.dealer_card_images[1].undraw()
            self.dealer_card_images[1] = Image(Point(850, 200), Game.get_card_image_file(self.dealer_hand.cards[1]))
            self.dealer_card_images[1].draw(Game.window)
            self.lbl_dealer_score.setText(f"Dealer Score: {self.dealer_hand.get_sum_bj()}")

            self.result_text.setText("The dealer got 21! You lost!")
            self.on_player_lose()

    def hit(self, event=None):

        # Draw a new card for the player
        if (not self.btn_hit.enabled) or self.hitting:
            return

        self.hitting = True

        Game.hitsound.play(loop=False, block=False)

        if self.player_hand.size() % 4 == 0:
            self.lbl_player_score.move(0, 80)
            self.player_score_moved_amount += 80

        self.player_hand.add_card(self.deck.draw())
        self.lbl_player_score.setText(f"Player Score: {self.player_hand.get_sum_bj()}")

        # make it so there are max 4 card by row, and the next row moves down by 80 pixels
        self.player_card_images.append(Image(Point(150 + (len(self.player_card_images) % 4) * 100, 200 +
                                                   (len(self.player_card_images) // 4) * 80),
                                             Game.get_card_image_file(self.player_hand.cards[-1])))
        self.player_card_images[-1].draw(Game.window)

        if self.player_hand.get_sum_bj() > 21:

            self.btn_hit.enabled = False
            self.hitting = False

            self.result_text.setText("You bust!")
            self.on_player_lose()

        elif self.player_hand.get_sum_bj() == 21 and self.dealer_hand.get_sum_bj() != 21:

            self.btn_hit.enabled = False
            self.hitting = False

            self.on_player_win(result_text="You got a Blackjack! You win!")

        elif self.player_hand.get_sum_bj == 21 and self.dealer_hand.get_sum_bj == 21:

            self.btn_hit.enabled = False
            self.hitting = False

            self.result_text.setText("You both got 21! It's a tie!")
            self.on_player_tie()

        else:
            self.hitting = False

    def stand(self, event=None):

        # End the player's turn and start the dealer's turn
        if not self.btn_stand.enabled:
            return

        self.btn_hit.enabled = False
        self.btn_stand.enabled = False

        Game.standsound.play(loop=False, block=False)
        self.dealer_turn()

    def dealer_turn(self):

        self.dealer_card_images[1].undraw()
        self.dealer_card_images[1] = Image(Point(850, 200), Game.get_card_image_file(self.dealer_hand.cards[1]))
        self.dealer_card_images[1].draw(Game.window)
        Game.window.tag_raise(self.dealer_card_images[1].id)
        self.lbl_dealer_score.setText(f"Dealer Score: {self.dealer_hand.get_sum_bj()}")

        while self.dealer_hand.get_sum_bj() < 17:

            time.sleep(0.8)

            if self.dealer_hand.size() % 4 == 0:
                self.lbl_dealer_score.move(0, 80)
                self.dealer_score_moved_amount += 80

            self.dealer_hand.add_card(self.deck.draw())
            self.dealer_card_images.append(Image(Point(750 + (len(self.dealer_card_images) % 4) * 100,
                                                       200 + (len(self.dealer_card_images) // 4) * 80),
                                                 Game.get_card_image_file(self.dealer_hand.cards[-1])))
            self.dealer_card_images[-1].draw(Game.window)
            self.lbl_dealer_score.setText(f"Dealer Score: {self.dealer_hand.get_sum_bj()}")

        if self.dealer_hand.get_sum_bj() > 21:

            self.on_player_win(result_text="Dealer Busts! You Win!")

        elif self.player_hand.get_sum_bj() > self.dealer_hand.get_sum_bj():

            self.on_player_win(result_text="Your hand is higher! You Win!")

        elif self.player_hand.get_sum_bj() < self.dealer_hand.get_sum_bj():

            self.result_text.setText("Dealer's hand is higher! You Lose!")
            self.on_player_lose()

        elif self.player_hand.get_sum_bj() == self.dealer_hand.get_sum_bj():

            self.result_text.setText("It's a tie!")
            self.on_player_tie()

    def bind_button_clicks(self):

        # Bind the event listeners to the buttons
        Game.close_btn.bind_click(Game.window, Game.close_win)
        self.btn_hit.bind_click(Game.window, self.hit)
        self.btn_stand.bind_click(Game.window, self.stand)
        self.btn_new_game.bind_click(Game.window, self.start_new_game)

    def on_player_win(self, result_text):

        Game.window.unbind_all("<Button-1>")
        edit_stats.add_win()

        time.sleep(1.5)

        undraw_all(Game.window)
        WinScreen.draw_screen(player_score=self.player_hand.get_sum_bj(), dealer_score=self.dealer_hand.get_sum_bj(),
                              result_text=result_text)

        self.result_text.draw(Game.window)
        Game.close_btn.draw(Game.window)
        Game.close_btn.bind_click(Game.window, Game.close_win)

    def on_player_lose(self):

        Game.window.unbind_all("<Button-1>")
        edit_stats.add_loss()

        time.sleep(1.5)

        undraw_all(Game.window)
        lose_window(Game.window, self.player_hand.get_sum_bj(), self.dealer_hand.get_sum_bj())

        self.result_text.draw(Game.window)
        Game.close_btn.draw(Game.window)
        Game.close_btn.bind_click(Game.window, Game.close_win)

    def on_player_tie(self):

        Game.window.unbind_all("<Button-1>")
        edit_stats.add_tie()

        time.sleep(1.5)

        undraw_all(Game.window)
        tie_window(Game.window, self.player_hand.get_sum_bj(), self.dealer_hand.get_sum_bj())

        self.result_text.draw(Game.window)
        Game.close_btn.draw(Game.window)
        Game.close_btn.bind_click(Game.window, Game.close_win)
