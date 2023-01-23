# File for some custom graphics things I made

from graphics import *
import typing


# Button class
class Button:
    # Create a button using two points, and a label
    def __init__(self, p1: Point, p2: Point, label: str):
        # Create the body of the button using a rectangle
        self.body = Rectangle(p1, p2)
        # Create text for the label
        self.label = Text(Point((p1.getX() + p2.getX()) / 2, (p1.getY() + p2.getY()) / 2), label)
        self.enabled = True

    # Function to draw the button
    def draw(self, window: GraphWin):
        self.body.draw(window)
        self.label.draw(window)
        window.items.append(self)

    # Function to undraw the button
    def undraw(self, window: GraphWin):
        self.body.undraw()
        self.label.undraw()
        window.items.remove(self)

    # Function to find a function to the button that gets executed when it is clicked
    def bind_click(self, win: GraphWin, fn: typing.Callable):
        win.tag_bind(self.body.id, "<Button-1>", fn)
        win.tag_bind(self.label.id, "<Button-1>", fn)

    # Function to unbind the click function
    def unbind_click(self, win: GraphWin):
        win.tag_unbind(self.body.id, "<Button-1>")
        win.tag_bind(self.label.id, "<Button-1>")

    # Function to determine if a point is inside the button
    def inside(self, click: Point) -> bool:
        p1x = min(self.body.getP1().getX(), self.body.getP2().getX())
        p1y = min(self.body.getP1().getY(), self.body.getP2().getY())
        p2x = max(self.body.getP1().getX(), self.body.getP2().getX())
        p2y = max(self.body.getP1().getY(), self.body.getP2().getY())
        return p1x < click.getX() < p2x and p1y < click.getY() < p2y

    # Function to move the button a layer up
    def move_top(self, window: GraphWin):
        window.tag_raise(self.body.id)
        window.tag_raise(self.label.id)


# Slider class
class Slider:
    # Create a slider using a center point, the length, the thickness, and the starting value
    def __init__(self, center: Point, length: int, thickness: int, starting_value: float):
        # Create the bottom part of the track
        self.track = Rectangle(Point(center.getX() - length / 2, center.getY() - thickness / 2),
                               Point(center.getX() + length / 2, center.getY() + thickness / 2))
        self.track.setFill(color_rgb(156, 156, 156))
        self.track.setOutline(color_rgb(156, 156, 156))

        # Create a circle to make the track rounded
        self.round_l = Circle(Point(center.getX() - length / 2, center.getY()), thickness / 2)
        self.round_l.setFill(color_rgb(0, 0, 0))
        self.round_l.setOutline(color_rgb(0, 0, 0))

        self.round_r = Circle(Point(center.getX() + length / 2, center.getY()), thickness / 2)
        self.round_r.setFill(color_rgb(156, 156, 156))
        self.round_r.setOutline(color_rgb(156, 156, 156))

        # Create the knob
        self.knob_pos = Point(center.getX() - length / 2 + length * starting_value, center.getY())
        self.knob = Circle(self.knob_pos, thickness)
        self.knob.setFill(color_rgb(0, 0, 0))
        self.knob.setOutline(color_rgb(0, 0, 0))

        # Create the top part of the track
        self.track_top = Rectangle(Point(center.getX() - length / 2, center.getY() - thickness / 2),
                                   Point(self.knob.getCenter().getX(), center.getY() + thickness / 2))
        self.track_top.setFill(color_rgb(0, 0, 0))
        self.track_top.setOutline(color_rgb(0, 0, 0))

        # Set the value of the slider
        self.value = starting_value

    # Function to draw the slider
    def draw(self, window: GraphWin):
        self.track.draw(window)
        self.round_l.draw(window)
        self.round_r.draw(window)
        self.track_top.draw(window)
        window.coords(self.track_top.id, self.track.getP1().getX(), self.track.getP1().getY(),
                      self.knob.getCenter().getX(), self.track.getP2().getY())
        self.knob.draw(window)
        window.items.append(self)

    # Function to undraw the slider
    def undraw(self, window: GraphWin):
        self.track.undraw()
        self.round_l.undraw()
        self.round_r.undraw()
        self.knob.undraw()
        self.track_top.undraw()
        window.items.remove(self)

    # Function the set the colour of the bottom part of the track
    def set_track_color(self, color: color_rgb):
        self.track.setFill(color)
        self.track.setOutline(color)
        self.round_r.setFill(color)
        self.round_r.setOutline(color)

    # Function to set the colour of the knob
    def set_knob_color(self, color: color_rgb):
        self.knob.setFill(color)
        self.knob.setOutline(color)

    # Function to set the colour of the top part of the track
    def set_top_track_color(self, color: color_rgb):
        self.track_top.setFill(color)
        self.track_top.setOutline(color)
        self.round_l.setFill(color)
        self.round_l.setOutline(color)

    # Function to determine if a point is inside the knob
    def inside_knob(self, click: Point) -> bool:
        return self.knob.getCenter().getX() - self.knob.getRadius() < click.getX() < self.knob.getCenter().getX() + \
            self.knob.getRadius() and \
            self.knob.getCenter().getY() - self.knob.getRadius() < click.getY() < self.knob.getCenter().getY() + \
            self.knob.getRadius()

    # Function to move the knob, and also resize the slider top
    def move_knob(self, event, fn: typing.Callable):
        from game import Game
        window = Game.window
        x_pos = event.x
        # Move the knob to the x-position
        if self.round_l.getCenter().getX() < x_pos < self.round_r.getCenter().getX():
            self.knob.move(x_pos - self.knob.getCenter().getX(), 0)

            # Resize the slider top
            window.coords(self.track_top.id, self.track_top.getP1().getX(), self.track_top.getP1().getY(), x_pos,
                          self.track_top.getP2().getY())

            self.value = (self.knob.getCenter().getX() - self.track.getP1().getX()) / \
                         (self.track.getP2().getX() - self.track.getP1().getX())

        # Function that gets called when the knob is clicked
        fn()

    # Function to bind the knob to a click
    def bind_click(self, win: GraphWin, fn: typing.Callable):
        win.tag_bind(self.knob.id, "<B1-Motion>", lambda event: self.move_knob(event, fn))
