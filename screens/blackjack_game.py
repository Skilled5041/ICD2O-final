# The blackjack game screen

from cards import *
from graphics import *
from graphics_extras import Button
from game import Game
from screens.result_screen import ResultScreen
from stats import edit_stats


# Class representing a game of blackjack
class BlackjackGame:
    # Initialise the blackjack screen
    # Initialise the deck, the player's hand, and the dealer's hand
    deck = None
    dealer_hand = None
    player_hand = None

    # Variable to track whether the hit function is currently being executed to prevent bugs
    task_executing = False

    # Tracks how much the score labels have moved, so when a new game is started, the labels can be moved back
    player_score_moved_amount = 0
    dealer_score_moved_amount = 0

    # Create the background
    bg = Image(Point(600, 400), "./images/bj_bg.png")

    # Create the hit button
    btn_hit = Button(Point(200, 620), Point(400, 700), "Hit")
    btn_hit.body.setFill("white")
    btn_hit.label.setSize(24)

    # Create the stand button
    btn_stand = Button(Point(500, 620), Point(700, 700), "Stand")
    btn_stand.body.setFill("white")
    btn_stand.label.setSize(24)

    # Create the new game button
    btn_new_game = Button(Point(800, 620), Point(1000, 700), "New Game")
    btn_new_game.body.setFill("white")
    btn_new_game.label.setSize(24)

    # List to store the images of the cards in the player's hand and the dealers hand
    player_card_images = []
    dealer_card_images = []

    # Labels to display the sum of the player's hand and the dealer's hand
    lbl_player_score = Text(Point(200, 350), "Player Score: 0")
    lbl_player_score.setTextColor("white")

    # The sum of the dealer's hand is hidden in the beginning
    lbl_dealer_score = Text(Point(800, 350), "Dealer Score: ???")
    lbl_dealer_score.setTextColor("white")

    # Button to return the previous screen
    back_btn = Button(Point(180, 700), Point(0, 800), "Back")
    back_btn.body.setFill("white")

    # Initialise a variable to track how long the user is playing
    start_time = int()

    # Function to go back to the start menu
    @staticmethod
    def return_to_start_screen(event=None):
        # If the button is disabled, do nothing
        if not BlackjackGame.back_btn.enabled:
            return
        # Play a sound and switch to the start screen
        Game.pop_sfx.play(block=False, loop=False)
        Game.undraw_all()
        from screens.start_screen import StartScreen
        StartScreen.start()

    # Function to draw the graphics objects onto the screen
    @staticmethod
    def draw_screen():

        BlackjackGame.bg.draw(Game.window)
        BlackjackGame.btn_hit.draw(Game.window)
        BlackjackGame.btn_stand.draw(Game.window)
        BlackjackGame.btn_new_game.draw(Game.window)
        BlackjackGame.lbl_player_score.draw(Game.window)
        BlackjackGame.lbl_dealer_score.draw(Game.window)
        BlackjackGame.back_btn.draw(Game.window)

        BlackjackGame.btn_new_game.enabled = True

    # Function to start a new game of blackjack
    @staticmethod
    def start_new_game(event=None):

        # If the button is disabled, do nothing or if a task is currently executing, do nothing (to prevent bugs)
        if BlackjackGame.task_executing or BlackjackGame.btn_new_game.enabled is False:
            return

        BlackjackGame.task_executing = True

        # Play a sound
        Game.new_game_sound.play()

        # Undraw the card images
        for image in BlackjackGame.player_card_images:
            image.undraw()
        for image in BlackjackGame.dealer_card_images:
            image.undraw()

        # Clear the list of card images
        BlackjackGame.player_card_images.clear()
        BlackjackGame.dealer_card_images.clear()

        # move the score labels back to the original position
        BlackjackGame.lbl_player_score.move(0, -BlackjackGame.player_score_moved_amount)
        BlackjackGame.lbl_dealer_score.move(0, -BlackjackGame.dealer_score_moved_amount)

        # Reset the moved amount variables
        BlackjackGame.player_score_moved_amount = 0
        BlackjackGame.dealer_score_moved_amount = 0

        # Re-enable the buttons
        BlackjackGame.btn_hit.enabled = True
        BlackjackGame.btn_stand.enabled = True
        BlackjackGame.btn_new_game.enabled = True
        BlackjackGame.back_btn.enabled = True

        # Bind the clicks to the buttons
        BlackjackGame.bind_button_clicks()

        # Create a hand for the player and dealer
        BlackjackGame.player_hand = Hand()
        BlackjackGame.dealer_hand = Hand()

        # Create the deck and shuffle it
        BlackjackGame.deck = Deck()
        BlackjackGame.deck.shuffle()

        # Deal two cards to the player and the dealer
        BlackjackGame.player_hand.add_card(BlackjackGame.deck.draw())
        BlackjackGame.player_hand.add_card(BlackjackGame.deck.draw())

        BlackjackGame.dealer_hand.add_card(BlackjackGame.deck.draw())
        BlackjackGame.dealer_hand.add_card(BlackjackGame.deck.draw())

        # Reset the text of the score labels
        BlackjackGame.lbl_player_score.setText(f"Player Score: {BlackjackGame.player_hand.get_sum_bj()}")
        BlackjackGame.lbl_dealer_score.setText(f"Dealer Score: ???")

        # Add the images of the cards to the list of card images
        BlackjackGame.player_card_images.append(
            Image(Point(150, 200), Game.get_card_image_file(BlackjackGame.player_hand.cards[0])))
        BlackjackGame.player_card_images.append(
            Image(Point(250, 200), Game.get_card_image_file(BlackjackGame.player_hand.cards[1])))

        # Draw the two cards in the player's hand
        BlackjackGame.player_card_images[0].draw(Game.window)
        BlackjackGame.player_card_images[1].draw(Game.window)

        # Add the images of the cards to the list of card images
        BlackjackGame.dealer_card_images.append(
            Image(Point(750, 200), Game.get_card_image_file(BlackjackGame.dealer_hand.cards[0])))
        BlackjackGame.dealer_card_images.append(Image(Point(850, 200), "./images/card_back.png"))

        # Draw the two cards in the dealer's hand
        BlackjackGame.dealer_card_images[0].draw(Game.window)
        BlackjackGame.dealer_card_images[1].draw(Game.window)

        # If the game is over (someone gets blackjack), end the game
        # Will reveal dealers card, and switch the results screens
        # Slightly different depending on if the player or dealer gets blackjack
        if BlackjackGame.player_hand.get_sum_bj() == 21 and BlackjackGame.dealer_hand.get_sum_bj() != 21:

            BlackjackGame.btn_hit.enabled = False

            # Show the dealer's hidden card
            BlackjackGame.dealer_card_images[1].undraw()
            BlackjackGame.dealer_card_images[1] = Image(Point(850, 200),
                                                        Game.get_card_image_file(BlackjackGame.dealer_hand.cards[1]))
            BlackjackGame.dealer_card_images[1].draw(Game.window)
            BlackjackGame.lbl_dealer_score.setText(f"Dealer Score: {BlackjackGame.dealer_hand.get_sum_bj()}")

            BlackjackGame.on_player_win(result_text="You got a Blackjack! You win!")

        elif BlackjackGame.player_hand.get_sum_bj() == 21 and BlackjackGame.dealer_hand.get_sum_bj() == 21:

            BlackjackGame.btn_hit.enabled = False

            # Show the dealer's hidden card
            BlackjackGame.dealer_card_images[1].undraw()
            BlackjackGame.dealer_card_images[1] = Image(Point(850, 200),
                                                        Game.get_card_image_file(BlackjackGame.dealer_hand.cards[1]))
            BlackjackGame.dealer_card_images[1].draw(Game.window)
            BlackjackGame.lbl_dealer_score.setText(f"Dealer Score: {BlackjackGame.dealer_hand.get_sum_bj()}")

            BlackjackGame.on_player_tie(result_text="You both got 21! It's a tie!")

        elif BlackjackGame.player_hand.get_sum_bj() != 21 and BlackjackGame.dealer_hand.get_sum_bj() == 21:

            BlackjackGame.btn_hit.enabled = False

            # Show the dealer's hidden card
            BlackjackGame.dealer_card_images[1].undraw()
            BlackjackGame.dealer_card_images[1] = Image(Point(850, 200),
                                                        Game.get_card_image_file(BlackjackGame.dealer_hand.cards[1]))
            BlackjackGame.dealer_card_images[1].draw(Game.window)
            BlackjackGame.lbl_dealer_score.setText(f"Dealer Score: {BlackjackGame.dealer_hand.get_sum_bj()}")

            BlackjackGame.on_player_lose("The dealer got 21! You lost!")

        else:
            # If the game is not over, set the start time
            BlackjackGame.start_time = time.time()

        BlackjackGame.task_executing = False

    # Function to hit
    @staticmethod
    def hit(event=None):

        # Draw a new card for the player
        if (not BlackjackGame.btn_hit.enabled) or BlackjackGame.task_executing:
            return

        BlackjackGame.task_executing = True

        # Play a sound
        Game.hit_sound.play(loop=False, block=False)

        # Depending on the size of the hand, move the label to allow space for row of cards, and track how much it moved
        if BlackjackGame.player_hand.size() % 4 == 0:
            BlackjackGame.lbl_player_score.move(0, 80)
            BlackjackGame.player_score_moved_amount += 80

        # Add the card to the player's hand and update the score label
        BlackjackGame.player_hand.add_card(BlackjackGame.deck.draw())
        BlackjackGame.lbl_player_score.setText(f"Player Score: {BlackjackGame.player_hand.get_sum_bj()}")

        # Make it so there are max 4 cards per row, and the next row moves down by 80 pixels
        BlackjackGame.player_card_images.append(
            Image(Point(150 + (len(BlackjackGame.player_card_images) % 4) * 100, 200 +
                        (len(BlackjackGame.player_card_images) // 4) * 80),
                  Game.get_card_image_file(BlackjackGame.player_hand.cards[-1])))
        BlackjackGame.player_card_images[-1].draw(Game.window)

        # If the player busts or gets blackjack, reveal the dealer's card and end the game
        # Slightly different depending on if the player gets blackjack or busts
        if BlackjackGame.player_hand.get_sum_bj() > 21:

            BlackjackGame.btn_hit.enabled = False
            BlackjackGame.btn_stand.enabled = False
            BlackjackGame.btn_new_game.enabled = False

            # Show the dealer's hidden card
            BlackjackGame.dealer_card_images[1].undraw()
            BlackjackGame.dealer_card_images[1] = Image(Point(850, 200),
                                                        Game.get_card_image_file(BlackjackGame.dealer_hand.cards[1]))
            BlackjackGame.dealer_card_images[1].draw(Game.window)
            BlackjackGame.lbl_dealer_score.setText(f"Dealer Score: {BlackjackGame.dealer_hand.get_sum_bj()}")

            BlackjackGame.on_player_lose(result_text="You bust!")

        elif BlackjackGame.player_hand.get_sum_bj() == 21 and BlackjackGame.dealer_hand.get_sum_bj() != 21:

            BlackjackGame.btn_hit.enabled = False
            BlackjackGame.btn_stand.enabled = False
            BlackjackGame.btn_new_game.enabled = False

            # Show the dealer's hidden card
            BlackjackGame.dealer_card_images[1].undraw()
            BlackjackGame.dealer_card_images[1] = Image(Point(850, 200),
                                                        Game.get_card_image_file(BlackjackGame.dealer_hand.cards[1]))
            BlackjackGame.dealer_card_images[1].draw(Game.window)
            BlackjackGame.lbl_dealer_score.setText(f"Dealer Score: {BlackjackGame.dealer_hand.get_sum_bj()}")

            BlackjackGame.on_player_win(result_text="You got a Blackjack! You win!")

        elif BlackjackGame.player_hand.get_sum_bj == 21 and BlackjackGame.dealer_hand.get_sum_bj == 21:

            BlackjackGame.btn_hit.enabled = False
            BlackjackGame.btn_stand.enabled = False
            BlackjackGame.btn_new_game.enabled = False

            # Show the dealer's hidden card
            BlackjackGame.dealer_card_images[1].undraw()
            BlackjackGame.dealer_card_images[1] = Image(Point(850, 200),
                                                        Game.get_card_image_file(BlackjackGame.dealer_hand.cards[1]))
            BlackjackGame.dealer_card_images[1].draw(Game.window)
            BlackjackGame.lbl_dealer_score.setText(f"Dealer Score: {BlackjackGame.dealer_hand.get_sum_bj()}")

            BlackjackGame.on_player_tie("You both got 21! It's a tie!")

        BlackjackGame.task_executing = False

    # Function to stand
    @staticmethod
    def stand(event=None):

        # End the player's turn and start the dealer's turn
        if not BlackjackGame.btn_stand.enabled or BlackjackGame.task_executing:
            return

        BlackjackGame.task_executing = True
        BlackjackGame.btn_hit.enabled = False
        BlackjackGame.btn_stand.enabled = False
        BlackjackGame.btn_new_game.enabled = False

        # Play a sound
        Game.stand_sound.play(loop=False, block=False)

        # Show the dealer's hidden card
        BlackjackGame.dealer_card_images[1].undraw()
        BlackjackGame.dealer_card_images[1] = Image(Point(850, 200),
                                                    Game.get_card_image_file(BlackjackGame.dealer_hand.cards[1]))
        BlackjackGame.dealer_card_images[1].draw(Game.window)
        Game.window.tag_raise(BlackjackGame.dealer_card_images[1].id)
        BlackjackGame.lbl_dealer_score.setText(f"Dealer Score: {BlackjackGame.dealer_hand.get_sum_bj()}")

        # Keep drawing cards until the dealer's score is 17 or higher
        while BlackjackGame.dealer_hand.get_sum_bj() < 17:

            time.sleep(0.8)

            # Depending on the size of the hand, move the label to allow space for row of cards,
            # and track how much it moved
            if BlackjackGame.dealer_hand.size() % 4 == 0:
                BlackjackGame.lbl_dealer_score.move(0, 80)
                BlackjackGame.dealer_score_moved_amount += 80

            # Add the card to the dealer's hand and update the score label
            BlackjackGame.dealer_hand.add_card(BlackjackGame.deck.draw())
            BlackjackGame.dealer_card_images.append(Image(Point(750 + (len(BlackjackGame.dealer_card_images) % 4) * 100,
                                                                200 + (
                                                                        len(BlackjackGame.dealer_card_images) // 4) * 80),
                                                          Game.get_card_image_file(
                                                              BlackjackGame.dealer_hand.cards[-1])))
            BlackjackGame.dealer_card_images[-1].draw(Game.window)
            BlackjackGame.lbl_dealer_score.setText(f"Dealer Score: {BlackjackGame.dealer_hand.get_sum_bj()}")

        # Depending on the value of the hands, will display a different result screen
        if BlackjackGame.dealer_hand.get_sum_bj() > 21:

            BlackjackGame.on_player_win(result_text="Dealer Busts! You Win!")

        elif BlackjackGame.player_hand.get_sum_bj() > BlackjackGame.dealer_hand.get_sum_bj():

            BlackjackGame.on_player_win(result_text="Your hand is higher! You Win!")

        elif BlackjackGame.player_hand.get_sum_bj() < BlackjackGame.dealer_hand.get_sum_bj():

            BlackjackGame.on_player_lose("Dealer's hand is higher! You Lose!")

        elif BlackjackGame.player_hand.get_sum_bj() == BlackjackGame.dealer_hand.get_sum_bj():

            BlackjackGame.on_player_tie("It's a tie!")

        else:
            BlackjackGame.btn_new_game.enabled = False

        BlackjackGame.task_executing = False

    # Function to bind the functions to the buttons
    @staticmethod
    def bind_button_clicks():

        # Bind the event listeners to the buttons
        BlackjackGame.btn_hit.bind_click(Game.window, BlackjackGame.hit)
        BlackjackGame.btn_stand.bind_click(Game.window, BlackjackGame.stand)
        BlackjackGame.btn_new_game.bind_click(Game.window, BlackjackGame.start_new_game)
        BlackjackGame.back_btn.bind_click(Game.window, BlackjackGame.return_to_start_screen)

    # Function to switch to the result screen
    @staticmethod
    def switch_screen(result_text, result):
        # Passes some info of the game to be displayed
        ResultScreen.draw_screen(player_score=BlackjackGame.player_hand.get_sum_bj(),
                                 dealer_score=BlackjackGame.dealer_hand.get_sum_bj(),
                                 result_text=result_text, result=result)

    # Function to display the result screen when the player wins
    @staticmethod
    def on_player_win(result_text):

        BlackjackGame.back_btn.enabled = False
        BlackjackGame.btn_new_game.enabled = False
        BlackjackGame.btn_hit.enabled = False
        BlackjackGame.btn_stand.enabled = False

        # Play a sound
        Game.win_sfx.play(loop=False, block=False)

        # Get the current time, and calculate the time difference between the current time and the start time
        # to track the elapsed time, and add it to the stats
        edit_stats.add_time(int(round(time.time() - BlackjackGame.start_time)))

        Game.window.unbind_all("<Button-1>")
        # Add 1 to the win count
        edit_stats.add_win()

        Game.window.after(1500, BlackjackGame.switch_screen, result_text, "win")

    # Basically the same as the on_player_win function, but for when the player loses
    @staticmethod
    def on_player_lose(result_text):

        BlackjackGame.back_btn.enabled = False
        BlackjackGame.btn_new_game.enabled = False
        BlackjackGame.btn_hit.enabled = False
        BlackjackGame.btn_stand.enabled = False

        Game.lose_sfx.play(loop=False, block=False)

        edit_stats.add_time(int(round(time.time() - BlackjackGame.start_time)))

        Game.window.unbind_all("<Button-1>")
        edit_stats.add_loss()

        Game.window.after(1500, BlackjackGame.switch_screen, result_text, "lose")

    # Basically the same as the on_player_win function, but for when the player ties
    @staticmethod
    def on_player_tie(result_text):

        BlackjackGame.back_btn.enabled = False
        BlackjackGame.btn_new_game.enabled = False
        BlackjackGame.btn_hit.enabled = False
        BlackjackGame.btn_stand.enabled = False

        edit_stats.add_time(int(round(time.time() - BlackjackGame.start_time)))

        Game.window.unbind_all("<Button-1>")
        edit_stats.add_tie()

        Game.window.after(1500, BlackjackGame.switch_screen, result_text, "tie")
