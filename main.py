from game import Game
from screens.start_screen import StartScreen


def main():

    from screens.settings_screen import SettingsScreen
    SettingsScreen.draw_screen()

    Game.mainloop()


main()
