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