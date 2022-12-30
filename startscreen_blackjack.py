from graphics import * 
import time

WIDTH = int(1200)
HEIGHT = int(800)


def create_opening_screen(window):
    background = Rectangle(Point(0, 0), Point(WIDTH, HEIGHT))
    background.setFill(color_rgb(166, 208, 240))
    background.draw(window)

    sidebar1_points = [Point(0, 0), Point(WIDTH / 8, HEIGHT / 8), Point(WIDTH / 10, HEIGHT), Point(0, HEIGHT)]
    sidebar1 = Polygon(sidebar1_points)
    sidebar1.setFill(color_rgb(91, 177, 243))
    sidebar1.draw(window)
    sidebar2_points = [Point(WIDTH, 0), Point(7 * WIDTH / 8, HEIGHT / 8), Point(9 * WIDTH / 10, HEIGHT),
                       Point(WIDTH, HEIGHT)]
    sidebar2 = Polygon(sidebar2_points)
    sidebar2.setFill(color_rgb(91, 177, 243))
    sidebar2.draw(window)

    title = Text(Point(WIDTH / 2, HEIGHT / 4), "Welcome to Blackjack!")
    title.setSize(32)
    title.setTextColor("white")
    title.draw(window)

    start_button = Rectangle(Point(WIDTH / 4 - 50, HEIGHT / 2 - 25), Point(WIDTH / 4 + 50, HEIGHT / 2 + 25))
    start_button.setFill("green")
    start_button.draw(window)

    line_left = Line(Point(145, 310), Point(180, 240))
    line_right = Line(Point(1030, 240), Point(1055, 310))
    line_middle = Line(Point(180, 240), Point(1030, 240))

    line_left.draw(window)
    line_right.draw(window)
    line_middle.draw(window)

    line_right.setWidth(5)
    line_left.setWidth(5)
    line_middle.setWidth(5)

    quit_button = Rectangle(Point(3 * WIDTH / 4 - 50, HEIGHT / 2 - 25), Point(3 * WIDTH / 4 + 50, HEIGHT / 2 + 25))
    quit_button.setFill("red")
    quit_button.draw(window)

    start_label = Text(start_button.getCenter(), "Start")
    start_label.draw(window)

    quit_label = Text(quit_button.getCenter(), "Quit")
    quit_label.draw(window)

    for i in range(37):
        time.sleep(0.01)
        sidebar1.move(20, 0)
        sidebar2.move(-20, 0)

    for i in range(37):
        time.sleep(0.01)
        sidebar1.move(-20, 0)
        sidebar2.move(20, 0)

    return start_button, quit_button, start_label, quit_label, title


def fade_out_opening_screen(start_button, quit_button, start_label, quit_label, title, window):
    for i in range(10):
        start_button.setFill(color_rgb(0, 255 - i * 25, 0))
        title.setTextColor(color_rgb(255 - i * 25, 255 - i * 25, 255 - i * 25))
        update(30)
    start_button.undraw()
    start_label.undraw()

    for i in range(10):
        quit_button.setFill(color_rgb(255 - i * 25, 0, 0))
        update(30)
    quit_button.undraw()
    quit_label.undraw()

    for i in range(10):
        title.setTextColor(color_rgb(255 - i * 25, 255 - i * 25, 255 - i * 25))
        update(30)
    title.undraw()

    for i in range(int(WIDTH / 2), 0, -10):
        rectangle1 = Rectangle(Point(i, 0), Point(i + 10, HEIGHT))
        rectangle1.setFill("white")
        rectangle1.draw(window)
        rectangle2 = Rectangle(Point(WIDTH - i - 10, 0), Point(WIDTH - i, HEIGHT))
        rectangle2.setFill("white")
        rectangle2.draw(window)
        update(100)

    for obj in window.items[:]:
        obj.undraw()
    window.update()


def start():
    window = GraphWin("Game", WIDTH, HEIGHT)
    window.setBackground("lightblue")
    start_button, quit_button, start_label, quit_label, title = create_opening_screen(window)

    while True:
        click_point = window.getMouse()
        if start_button.getP1().getX() < click_point.getX() < start_button.getP2().getX() and \
                start_button.getP1().getY() < click_point.getY() < start_button.getP2().getY():
            fade_out_opening_screen(start_button, quit_button, start_label, quit_label, title, window)
            window.close()

        elif quit_button.getP1().getX() < click_point.getX() < quit_button.getP2().getX() and \
                quit_button.getP1().getY() < click_point.getY() < quit_button.getP2().getY():
            fade_out_opening_screen(start_button, quit_button, start_label, quit_label, title, window)
            print("quit")
            window.close()
            break
        else:
            print("Else")


start()
