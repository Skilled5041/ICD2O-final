from graphics import *
import typing


class Button:
    def __init__(self, p1: Point, p2: Point, label: str):
        self.body = Rectangle(p1, p2)
        self.label = Text(Point((p1.getX() + p2.getX()) / 2, (p1.getY() + p2.getY()) / 2), label)
        self.enabled = True

    def draw(self, window: GraphWin):
        self.body.draw(window)
        self.label.draw(window)
        window.items.append(self)

    def undraw(self, window: GraphWin):
        self.body.undraw()
        self.label.undraw()
        window.items.remove(self)

    def bind_click(self, win: GraphWin, fn: typing.Callable):
        win.tag_bind(self.body.id, "<Button-1>", fn)
        win.tag_bind(self.label.id, "<Button-1>", fn)

    def unbind_click(self, win: GraphWin):
        win.tag_unbind(self.body.id, "<Button-1>")
        win.tag_bind(self.label.id, "<Button-1>")

    def inside(self, click: Point) -> bool:
        p1x = min(self.body.getP1().getX(), self.body.getP2().getX())
        p1y = min(self.body.getP1().getY(), self.body.getP2().getY())
        p2x = max(self.body.getP1().getX(), self.body.getP2().getX())
        p2y = max(self.body.getP1().getY(), self.body.getP2().getY())
        return p1x < click.getX() < p2x and p1y < click.getY() < p2y

    def move_top(self, window: GraphWin):
        window.tag_raise(self.body.id)
        window.tag_raise(self.label.id)


class Slider:
    def __init__(self, center: Point, length: int, thickness: int, starting_value: float):
        self.track = Rectangle(Point(center.getX() - length / 2, center.getY() - thickness / 2),
                               Point(center.getX() + length / 2, center.getY() + thickness / 2))
        self.track.setFill(color_rgb(156, 156, 156))
        self.track.setOutline(color_rgb(156, 156, 156))

        self.round_l = Circle(Point(center.getX() - length / 2, center.getY()), thickness / 2)
        self.round_l.setFill(color_rgb(0, 0, 0))
        self.round_l.setOutline(color_rgb(0, 0, 0))

        self.round_r = Circle(Point(center.getX() + length / 2, center.getY()), thickness / 2)
        self.round_r.setFill(color_rgb(156, 156, 156))
        self.round_r.setOutline(color_rgb(156, 156, 156))

        self.knob_pos = Point(center.getX() - length / 2 + length * starting_value, center.getY())
        self.knob = Circle(self.knob_pos, thickness)
        self.knob.setFill(color_rgb(0, 0, 0))
        self.knob.setOutline(color_rgb(0, 0, 0))

        self.track_top = Rectangle(Point(center.getX() - length / 2, center.getY() - thickness / 2),
                                   Point(self.knob.getCenter().getX(), center.getY() + thickness / 2))
        self.track_top.setFill(color_rgb(0, 0, 0))
        self.track_top.setOutline(color_rgb(0, 0, 0))

        self.value = starting_value

    def draw(self, window: GraphWin):
        self.track.draw(window)
        self.round_l.draw(window)
        self.round_r.draw(window)
        self.track_top.draw(window)
        window.coords(self.track_top.id, self.track.getP1().getX(), self.track.getP1().getY(),
                      self.knob.getCenter().getX(), self.track.getP2().getY())
        self.knob.draw(window)
        window.items.append(self)

    def undraw(self, window: GraphWin):
        self.track.undraw()
        self.round_l.undraw()
        self.round_r.undraw()
        self.knob.undraw()
        self.track_top.undraw()
        window.items.remove(self)

    def set_track_color(self, color: color_rgb):
        self.track.setFill(color)
        self.track.setOutline(color)
        self.round_r.setFill(color)
        self.round_r.setOutline(color)

    def set_knob_color(self, color: color_rgb):
        self.knob.setFill(color)
        self.knob.setOutline(color)

    def set_top_track_color(self, color: color_rgb):
        self.track_top.setFill(color)
        self.track_top.setOutline(color)
        self.round_l.setFill(color)
        self.round_l.setOutline(color)

    def inside_knob(self, click: Point) -> bool:
        return self.knob.getCenter().getX() - self.knob.getRadius() < click.getX() < self.knob.getCenter().getX() + \
            self.knob.getRadius() and \
            self.knob.getCenter().getY() - self.knob.getRadius() < click.getY() < self.knob.getCenter().getY() + \
            self.knob.getRadius()

    def move_knob(self, event, fn: typing.Callable):
        from game import Game
        window = Game.window
        x_pos = event.x
        if self.round_l.getCenter().getX() < x_pos < self.round_r.getCenter().getX():
            self.knob.move(x_pos - self.knob.getCenter().getX(), 0)

            window.coords(self.track_top.id, self.track_top.getP1().getX(), self.track_top.getP1().getY(), x_pos,
                          self.track_top.getP2().getY())

            self.value = (self.knob.getCenter().getX() - self.track.getP1().getX()) / \
                         (self.track.getP2().getX() - self.track.getP1().getX())

        fn()

    def bind_click(self, win: GraphWin, fn: typing.Callable):
        win.tag_bind(self.knob.id, "<B1-Motion>", lambda event: self.move_knob(event, fn))
