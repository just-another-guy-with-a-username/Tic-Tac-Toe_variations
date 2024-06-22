import time
from cell import Cell

class Board():
    def __init__(self, cell_size, x1, y1, win=None):
        self._dimensions = 3
        self._cell_size = cell_size
        self._x1 = x1
        self._y1 = y1
        self._win = win
        self._cells = []
        self._create_cells()

    def _create_cells(self):
        for i in range(self._dimensions):
            col_cells = []
            for j in range(self._dimensions):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._dimensions):
            for j in range(self._dimensions):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size
        y1 = self._y1 + j * self._cell_size
        x2 = x1 + self._cell_size
        y2 = y1 + self._cell_size
        if i == 0:
            self._cells[i][j].has_left_wall = False
        if i == self._dimensions - 1:
            self._cells[i][j].has_right_wall = False
        if j == 0:
            self._cells[i][j].has_top_wall = False
        if j == self._dimensions - 1:
            self._cells[i][j].has_bottom_wall = False
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
