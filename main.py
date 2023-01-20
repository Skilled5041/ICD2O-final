from game import Game
from screens.blackjack_game import BlackjackGame
from screens.start_screen import StartScreen


def main():
    # Main function for program
    # BlackjackGame.draw_screen()
    # BlackjackGame.start_new_game()

    StartScreen.start()

    Game.mainloop()


main()
