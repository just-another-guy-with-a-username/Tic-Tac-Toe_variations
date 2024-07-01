import tkinter as tk


class Window:
    def __init__(self, width, height):
        self.__root = tk.Tk()
        self.__root.title("Tick-oaT-Two")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = tk.Canvas(self.__root, bg="black", height=height, width=width)
        self.__canvas.pack(fill=tk.BOTH, expand=1)
        self.__running = False
        self._width = width
        self._height = height

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def draw_line(self, line, fill_color="#00FF00"):
        line.draw(self.__canvas, fill_color)

    def close(self):
        self.__running = False

    def get_root(self):
        return self.__root

    def get_canvas(self):
        return self.__canvas

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(
        self,
        p1,
        p2,
    ):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color="#00FF00"):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )
