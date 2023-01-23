# Final ICS201 Project
# A single-player game that includes blackjack and slapjack
# Aaron and Calvin
# 2023/01/22

# Type this in a terminal to install the required packages:
# pip3 install -r requirements.txt

from game import Game
from screens.start_screen import StartScreen


def main():

    # Display the start screen
    StartScreen.start()

    Game.mainloop()


main()
