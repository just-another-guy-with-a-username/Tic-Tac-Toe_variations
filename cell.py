from graphics import Point, Line

class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.vertical = False
        self.horizontal = False
        self.allowed_horizontal = True
        self.allowed_vertical = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line, "black")
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line, "black")
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line, "black")
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line, "black")

    def draw_vertical(self):
        x_average = (self._x1 + self._x2) / 2
        y_difference = (self._y1 - self._y2) / 8
        line = Line(Point(x_average, self._y1 - y_difference), Point(x_average, self._y2 + y_difference))
        self._win.draw_line(line)

    def draw_horizontal(self):
        y_average = (self._y1 + self._y2) / 2
        x_difference = (self._x1 - self._x2) / 8
        line = Line(Point(self._x1 - x_difference, y_average), Point(self._x2 + x_difference, y_average))
        self._win.draw_line(line)
