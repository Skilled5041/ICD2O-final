from game import Game
from screens.blackjack_game import BlackjackGame


def main():
    # Main function for program
    BlackjackGame.draw_screen()
    BlackjackGame.start_new_game()

    Game.mainloop()


main()
