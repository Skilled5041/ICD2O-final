from game import Game
from blackjack_game import BlackjackGame


def main():
    # Main function for program
    bj_game = BlackjackGame()
    bj_game.draw_screen()
    bj_game.start_new_game()

    Game.mainloop()


main()
