from graphics import *
from graphics_extras import Button
from game import Game


# Result screen class
class ResultScreen:
    # Different result messages and colours depending on the result
    result_message = {
        "win": "You win!",
        "lose": "You lose!",
        "tie": "It's a tie!"
    }

    bg_colours = {
        "win": color_rgb(140, 215, 255),
        "lose": color_rgb(255, 143, 143),
        "tie": color_rgb(174, 183, 191)
    }

    # Create the graphics objects
    result = Text(Point(600, 200), "")
    result.setStyle('bold')
    result.setSize(36)

    new_game_btn = Button(Point(250, 400), Point(450, 500), "New Game")
    new_game_btn.body.setFill("green")
    new_game_btn.label.setSize(24)

    main_menu_btn = Button(Point(750, 400), Point(950, 500), "Quit")
    main_menu_btn.body.setFill("red")
    main_menu_btn.label.setSize(24)

    scores = Text(Point(600, 300), "")
    scores.setSize(24)

    result_text = Text(Point(600, 650), "")
    result_text.setSize(36)

    # Draw the screen and bind the clicks, also update the text
    @staticmethod
    def draw_screen(player_score, dealer_score, result_text, result):
        Game.undraw_all()
        Game.current_screen = "result"

        Game.window.setBackground(ResultScreen.bg_colours[result])
        ResultScreen.scores.setText(f"Your score: {player_score} \nDealer score: {dealer_score}")
        ResultScreen.result_text.setText(result_text)
        ResultScreen.result.setText(ResultScreen.result_message[result])

        ResultScreen.result.draw(Game.window)
        ResultScreen.new_game_btn.draw(Game.window)
        ResultScreen.main_menu_btn.draw(Game.window)
        ResultScreen.scores.draw(Game.window)
        ResultScreen.result_text.draw(Game.window)

        ResultScreen.bind_button_clicks()

    # Switch the screen to the blackjack game
    @staticmethod
    def switch_to_blackjack(event=None):
        from screens.blackjack_game import BlackjackGame
        Game.undraw_all()
        BlackjackGame.draw_screen()
        BlackjackGame.start_new_game()

    # Switch the screen to the main menu
    @staticmethod
    def switch_to_main_menu(event=None):
        Game.pop_sfx.play(loop=False, block=False)
        from screens.start_screen import StartScreen
        Game.undraw_all()
        StartScreen.start()

    # Function to bind all the button clicks
    @staticmethod
    def bind_button_clicks():
        ResultScreen.new_game_btn.bind_click(Game.window, ResultScreen.switch_to_blackjack)
        ResultScreen.main_menu_btn.bind_click(Game.window, ResultScreen.switch_to_main_menu)
