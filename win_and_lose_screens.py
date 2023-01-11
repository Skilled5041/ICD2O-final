from graphics import *
from graphics_elements import Button
import sys


def win_window(window, player_score, dealer_score):
    window.setBackground(color_rgb(113, 203, 255))

    win_message = Text(Point(600, 200), "Congrats, you won!")
    win_message.setStyle('bold')
    win_message.setSize(36)
    win_message.draw(window)

    new_game_btn = Button(Point(250, 400), Point(450, 500), "New Game")
    new_game_btn.body.setFill("green")
    new_game_btn.label.setSize(24)
    new_game_btn.draw(window)

    main_menu_btn = Button(Point(750, 400), Point(950, 500), "Quit")
    main_menu_btn.body.setFill("red")
    main_menu_btn.label.setSize(24)
    main_menu_btn.draw(window)

    scores = Text(Point(600, 300), f"Your score: {player_score}\nDealer score: {dealer_score}")
    scores.setSize(24)
    scores.draw(window)

    """Add later"""


def lose_window(window, player_score, dealer_score):
    window.setBackground(color_rgb(255, 204, 203))

    lost_message = Text(Point(600, 200), "You Lost :(")
    lost_message.setStyle('bold')
    lost_message.setSize(36)
    lost_message.draw(window)

    new_game_btn = Button(Point(250, 400), Point(450, 500), "New Game")
    new_game_btn.body.setFill("green")
    new_game_btn.label.setSize(24)
    new_game_btn.draw(window)

    main_menu_btn = Button(Point(750, 400), Point(950, 500), "Quit")
    main_menu_btn.body.setFill("red")
    main_menu_btn.label.setSize(24)
    main_menu_btn.draw(window)

    scores = Text(Point(600, 300), f"Your score: {player_score}\nDealer score: {dealer_score}")
    scores.setSize(24)
    scores.draw(window)

    """Add later"""


def tie_window(window, player_score, dealer_score):
    window.setBackground(color_rgb(150, 150, 150))

    tie_message = Text(Point(600, 200), "It's a Tie!")
    tie_message.setStyle('bold')
    tie_message.setSize(36)
    tie_message.draw(window)

    new_game_btn = Button(Point(250, 400), Point(450, 500), "New Game")
    new_game_btn.body.setFill("green")
    new_game_btn.label.setSize(24)
    new_game_btn.draw(window)

    main_menu_btn = Button(Point(750, 400), Point(950, 500), "Quit")
    main_menu_btn.body.setFill("red")
    main_menu_btn.label.setSize(24)
    main_menu_btn.draw(window)

    scores = Text(Point(600, 300), f"Your score: {player_score}\nDealer score: {dealer_score}")
    scores.setSize(24)
    scores.draw(window)

    """Add later"""


def exit_window(event=None):
    sys.exit()
