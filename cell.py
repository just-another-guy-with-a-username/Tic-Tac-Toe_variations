from graphics import Point, Line


class Cell:
    def __init__(self, x1, x2, y1, y2, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._vertical = False
        self._horizontal = False
        self._allowed_horizontal = True
        self._allowed_vertical = True
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win

    def draw(self):
        if self._win is None:
            return
        if self.has_left_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line, "black")
        if self.has_top_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self._win.draw_line(line)
        else:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self._win.draw_line(line, "black")
        if self.has_right_wall:
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            self._win.draw_line(line, "black")
        if self.has_bottom_wall:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
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

    def reset(self):
        self._vertical = False
        self._horizontal = False
        self._allowed_horizontal = True
        self._allowed_vertical = True
        x_average = (self._x1 + self._x2) / 2
        y_difference = (self._y1 - self._y2) / 8
        line = Line(Point(x_average, self._y1 - y_difference), Point(x_average, self._y2 + y_difference))
        self._win.draw_line(line, "black")
        y_average = (self._y1 + self._y2) / 2
        x_difference = (self._x1 - self._x2) / 8
        line = Line(Point(self._x1 - x_difference, y_average), Point(self._x2 + x_difference, y_average))
        self._win.draw_line(line, "black")
