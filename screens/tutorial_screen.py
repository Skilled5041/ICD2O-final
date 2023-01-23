from graphics import *
from graphics_extras import Button
from game import Game
import webbrowser


# Tutorial screen class
class TutorialScreen:
    # Create the buttons
    instructions_blackjack = Button(Point(300, 200), Point(500, 300), "Blackjack Game Rules")
    instructions_blackjack.body.setFill("green")
    instructions_blackjack.label.setSize(12)
    instructions_slapjack = Button(Point(700, 200), Point(900, 300), "Slapjack Game Rules")
    instructions_slapjack.body.setFill("blue")
    instructions_slapjack.label.setSize(12)
    instructions_slapjack.label.setTextColor("white")

    other_instructions = Text(Point(600, 500), "Other Instructions:\n"
                                               "You can change the volume of the music and sound effects"
                                               " in the main menu which is found in the start screen.\n"
                                               "You can view your blackjack stats in the stats menu which"
                                               " can be accessed through the start menu.\n"
                                               "You can reset your stat inside the stats menu.\n"
                                               "After pressing start, in the start menu, you can choose"
                                               "which game you want to play (slapjack is not finished).\n"
                                               "When playing blackjack, click the onscreen buttons to hit, stand or "
                                               "start a new game.\n")
    other_instructions.setSize(14)

    back_btn = Button(Point(0, 600), Point(200, 700), "Back")
    back_btn.body.setFill("white")

    # Plays a pop sound then executes a function
    @staticmethod
    def play_pop(fn):
        Game.pop_sfx.play(loop=False, block=False)
        fn()

    # Function to open a link in the browser
    @staticmethod
    def open_link(link):
        webbrowser.open_new_tab(link)

    # Draw everything onto the screen adn bind the clicks
    @staticmethod
    def draw_screen(event=None):
        Game.undraw_all()

        TutorialScreen.instructions_blackjack.draw(Game.window)
        TutorialScreen.back_btn.draw(Game.window)
        TutorialScreen.instructions_slapjack.draw(Game.window)
        TutorialScreen.other_instructions.draw(Game.window)

        TutorialScreen.instructions_blackjack.bind_click(Game.window, lambda _: TutorialScreen.open_link(
            "https://bicyclecards.com/how-to-play/blackjack/"))
        TutorialScreen.instructions_slapjack.bind_click(Game.window, lambda _: TutorialScreen.open_link(
            "https://bicyclecards.com/how-to-play/slapjack/"))

        from screens.start_screen import StartScreen
        TutorialScreen.back_btn.bind_click(Game.window, lambda _: TutorialScreen.play_pop(StartScreen.start))
