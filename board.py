import tkinter as tk
from cell import Cell
from graphics import Line, Point
import random
import time



class Board():
    def __init__(self, cell_size, x1, y1, win=None):
        self._dimensions = 3
        self._cell_size = cell_size
        self._x1 = x1
        self._y1 = y1
        self._win = win
        self._cells = []
        self._buttons = []
        self._vertical_turn = True
        self._vertical_score = 0
        self._horizontal_score = 0
        self.close = None
        self.replay = None
        self.menu = None
        self.win_lines = []
        self._vertical_score_teller = None
        self._horizontal_score_teller = None
        self.display_scores()
        self._create_cells_and_buttons()

    def _create_cells_and_buttons(self):
        for i in range(self._dimensions):
            col_cells = []
            for j in range(self._dimensions):
                x1 = self._x1 + i * self._cell_size
                y1 = self._y1 + j * self._cell_size
                x2 = x1 + self._cell_size
                y2 = y1 + self._cell_size
                col_cells.append(Cell(x1, x2, y1, y2, self._win))
            self._cells.append(col_cells)
        for i in range(self._dimensions):
            col_buttons = []
            for j in range(self._dimensions):
                col_buttons.append(tk.Button(self._win.get_root(), bg="#00FF00", activebackground="#009000", borderwidth=0,
                                             command=lambda i=i, j=j: self.move(i, j)))
            self._buttons.append(col_buttons)
        for i in range(self._dimensions):
            for j in range(self._dimensions):
                self._draw_cell_and_button(i, j)

    def _draw_cell_and_button(self, i, j):
        if self._win is None:
            return
        if i == 0:
            self._cells[i][j].has_left_wall = False
        if i == self._dimensions - 1:
            self._cells[i][j].has_right_wall = False
        if j == 0:
            self._cells[i][j].has_top_wall = False
        if j == self._dimensions - 1:
            self._cells[i][j].has_bottom_wall = False
        self._cells[i][j].draw()
        x1 = self._x1 + i * self._cell_size
        y1 = self._y1 + j * self._cell_size
        x2 = x1 + self._cell_size
        y2 = y1 + self._cell_size
        self._buttons[i][j].place(x=x1+(self._cell_size*self._dimensions)+(self._cell_size/3),
                                  y=y1+(self._cell_size/3),
                                  height=self._cell_size/3,
                                  width=self._cell_size/3)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()

    def move(self, i, j):
        cell = self._cells[i][j]
        if self._vertical_turn:
            self.vertical_move(cell, i, j)
        else:
            self.horizontal_move(cell, i, j)

    def vertical_move(self, cell, i, j):
        if cell._allowed_vertical and not cell._vertical:
            self._cells[i][j].draw_vertical()
            self._cells[i][j]._vertical = True
            self._vertical_turn = False
            for col in self._cells:
                for space in col:
                    space._allowed_horizontal = True
            self._cells[i][j]._allowed_horizontal = False
            win = self.check_win()
            if win != 0:
                if win == 1:
                    print("Vertical wins!")
                else:
                    print(f"Vertical wins with {win} lines!")
                for col in self._buttons:
                    for button in col:
                        button["state"] = "disabled"
                self._vertical_score += 1
                self.display_scores()
                self.end_buttons()
                return True
        else:
            print("Illegal Move Found!")

    def horizontal_move(self, cell, i, j):
        if cell._allowed_horizontal and not cell._horizontal:
            self._cells[i][j].draw_horizontal()
            self._cells[i][j]._horizontal = True
            self._vertical_turn = True
            for col in self._cells:
                for space in col:
                    space._allowed_vertical = True
            self._cells[i][j]._allowed_vertical = False
            win = self.check_win()
            if win != 0:
                if win == 1:
                    print("Horizontal wins!")
                else:
                    print(f"Horizontal wins with {win} lines!")
                for col in self._buttons:
                    for button in col:
                        button["state"] = "disabled"
                self._horizontal_score += 1
                self.display_scores()
                self.end_buttons()
        else:
            print("Illegal Move Found!")

    def check_win(self):
         win_count = 0
         for i in range(0, self._dimensions):
             if (self._cells[i][0]._vertical==True and self._cells[i][0]._horizontal==True and
                 self._cells[i][1]._vertical==True and self._cells[i][1]._horizontal==True and
                 self._cells[i][2]._vertical==True and self._cells[i][2]._horizontal==True):
                 win_count += 1
                 self._win.draw_line(Line(Point(self._cells[i][0]._x1+self._cell_size/2, self._cells[i][0]._y1),
                                          Point(self._cells[i][0]._x1+self._cell_size/2, self._cells[i][2]._y2)))
                 self.win_lines.append(Line(Point(self._cells[i][0]._x1+self._cell_size/2, self._cells[i][0]._y1),
                                            Point(self._cells[i][0]._x1+self._cell_size/2, self._cells[i][2]._y2)))
         for i in range(0, self._dimensions):
             if (self._cells[0][i]._vertical==True and self._cells[0][i]._horizontal==True and
                 self._cells[1][i]._vertical==True and self._cells[1][i]._horizontal==True and
                 self._cells[2][i]._vertical==True and self._cells[2][i]._horizontal==True):
                 win_count += 1
                 self._win.draw_line(Line(Point(self._cells[0][i]._x1, self._cells[0][i]._y1+self._cell_size/2),
                                          Point(self._cells[2][i]._x2, self._cells[0][i]._y1+self._cell_size/2)))
                 self.win_lines.append(Line(Point(self._cells[0][i]._x1, self._cells[0][i]._y1+self._cell_size/2),
                                            Point(self._cells[2][i]._x2, self._cells[0][i]._y1+self._cell_size/2)))
         if (self._cells[0][0]._vertical==True and self._cells[0][0]._horizontal==True and
             self._cells[1][1]._vertical==True and self._cells[1][1]._horizontal==True and
             self._cells[2][2]._vertical==True and self._cells[2][2]._horizontal==True):
             win_count += 1
             self._win.draw_line(Line(Point(self._cells[0][0]._x1, self._cells[0][0]._y1),
                                      Point(self._cells[2][2]._x2, self._cells[2][2]._y2)))
             self.win_lines.append(Line(Point(self._cells[0][0]._x1, self._cells[0][0]._y1),
                                        Point(self._cells[2][2]._x2, self._cells[2][2]._y2)))
         if (self._cells[0][2]._vertical==True and self._cells[0][2]._horizontal==True and
             self._cells[1][1]._vertical==True and self._cells[1][1]._horizontal==True and
             self._cells[2][0]._vertical==True and self._cells[2][0]._horizontal==True):
             win_count += 1
             self._win.draw_line(Line(Point(self._cells[2][0]._x2, self._cells[2][0]._y1),
                                      Point(self._cells[0][2]._x1, self._cells[0][2]._y2)))
             self.win_lines.append(Line(Point(self._cells[2][0]._x2, self._cells[2][0]._y1),
                                        Point(self._cells[0][2]._x1, self._cells[0][2]._y2)))
         return win_count

    def end_buttons(self):
        self.close = tk.Button(bg="#00C000", activebackground="#009000", borderwidth=0, text="Close",
                               anchor="center", command=self.end_program)
        self.close.place(width=self._win._width/3, height=self._win._height/30,
                         x=self._win._width/3, y=(self._win._height/2)-(self._win._height/15))
        self.replay = tk.Button(bg="#00C000", activebackground="#009000", borderwidth=0, text="Play Again",
                                anchor="center", command=self.reset_board)
        self.replay.place(width=self._win._width/3, height=self._win._height/30,
                          x=self._win._width/3, y=(self._win._height/2)-(self._win._height/45))
        self.menu = tk.Button(bg="#00C000", activebackground="#009000", borderwidth=0, text="Main Menu",
                                anchor="center", command=self.main_menu)
        self.menu.place(width=self._win._width/3, height=self._win._height/30,
                          x=self._win._width/3, y=(self._win._height/2)+(self._win._height/45))

    def end_program(self):
        self._win.get_root().destroy()

    def reset_board(self):
        self.close.destroy()
        self.replay.destroy()
        self.menu.destroy()
        for col in self._buttons:
            for button in col:
                button["state"] = "normal"
        for line in self.win_lines:
            self._win.draw_line(line, "black")
        for col in self._cells:
            for cell in col:
                cell.reset()
                cell.draw()

    def main_menu(self):
        self.close.destroy()
        self.replay.destroy()
        self.menu.destroy()
        self._vertical_score_teller.destroy()
        self._horizontal_score_teller.destroy()
        for col in self._buttons:
            for button in col:
                button.destroy()
        for line in self.win_lines:
            self._win.draw_line(line, "black")
        for col in self._cells:
            for cell in col:
                cell.reset()
                cell.disappear()
        window_length = self._win._width
        window_height = self._win._height
        button1 = tk.Button(self._win.get_root(), bg="#00C000", activebackground="#009000", text="Local Multiplayer",
                            anchor="center")
        button2 = tk.Button(self._win.get_root(), bg="#00C000", activebackground="#009000", text="Singleplayer",
                            anchor="center")
        button1['command'] = lambda button1=button1, button2=button2, win=self._win: make_board(button1, button2, win)
        button2['command'] = lambda button1=button1, button2=button2, win=self._win: make_AI_board(button1, button2, win)
        button1.place(x=window_length/3, y=window_height/5, width=window_length/3, height=window_height/5)
        button2.place(x=window_length/3, y=(window_height/5)*3, width=window_length/3, height=window_height/5)

    def display_scores(self):
        vertical_score = tk.StringVar()
        vertical_score.set(f"Vertical wins: {self._vertical_score}")
        self._vertical_score_teller = tk.Label(height=1, width=100, bg="#00FF00", fg="black",
                                               textvariable=vertical_score)
        horizontal_score = tk.StringVar()
        horizontal_score.set(f"Horizontal wins: {self._horizontal_score}")
        self._horizontal_score_teller = tk.Label(height=1, width=100, bg="#00FF00", fg="black",
                                                 textvariable=horizontal_score)
        self._vertical_score_teller.place(x=2, y=22)
        self._horizontal_score_teller.place(x=2, y=42)

class AI_Board(Board):
    def __init__(self, cell_size, x1, y1, win=None):
        super().__init__(cell_size, x1, y1, win)
        self.d_board = [[[False, False], [True, True], [False, False]],
                        [[True, True], [False, False], [True, True]],
                        [[False, False], [True, True], [False, False]]]

    def reset_board(self):
        super().reset_board()
        self.d_board = [[[False, False], [True, True], [False, False]],
                        [[True, True], [False, False], [True, True]],
                        [[False, False], [True, True], [False, False]]]

    def move(self, i, j):
        cell = self._cells[i][j]
        if self._vertical_turn:
            move = self.vertical_move(cell, i, j)
        if move!=True:
            self._win.redraw()
            time.sleep(1)
            AI_move = self.best_move()
            if AI_move != None and not self._vertical_turn:
                self.horizontal_move(self._cells[AI_move[0]][AI_move[1]], AI_move[0], AI_move[1])
            self._vertical_turn = True

    def best_move(self):
        win_lines = []
        for i in range(0, self._dimensions):
            if (self._cells[i][0]._vertical==True and
                self._cells[i][1]._vertical==True and
                self._cells[i][2]._vertical==True):
                win_lines.append([[i, 0], [i, 1], [i, 2]])
        for i in range(0, self._dimensions):
            if (self._cells[0][i]._vertical==True and
                self._cells[1][i]._vertical==True and
                self._cells[2][i]._vertical==True):
                win_lines.append([[0, i], [1, i], [2, i]])
        if (self._cells[0][0]._vertical==True and
            self._cells[1][1]._vertical==True and
            self._cells[2][2]._vertical==True):
            win_lines.append([[0, 0], [1, 1], [2, 2]])
        if (self._cells[0][2]._vertical==True and
            self._cells[1][1]._vertical==True and
            self._cells[2][0]._vertical==True):
            win_lines.append([[0, 2], [1, 1], [2, 0]])
        if win_lines != []:
            for line in win_lines:
                for cell in line:
                    if not self._cells[cell[0]][cell[1]]._horizontal and self._cells[cell[0]][cell[1]]._allowed_horizontal:
                        return cell
        c_board = []
        for col in self._cells:
            c_col = []
            for cell in col:
                c_col.append([cell._vertical, cell._horizontal])
            c_board.append(c_col)
        if c_board[1][0]==[True, True] and c_board[0][1]==[True, True] and c_board[1][2]==[True, True] and c_board[2][1]==[True, True]:
            if (c_board[0][0]==[True, True] and c_board[2][2]==[True, True]) or (c_board[0][2]==[True, True] and c_board[2][0]==[True, True]):
                if c_board[1][1][1]==True or c_board[1][1][0]==True:
                    if c_board[0][0][1]==False:
                        if self._cells[0][0]._allowed_horizontal==True:
                            return[0, 0]
                    if c_board[2][0][1]==False:
                        if self._cells[2][0]._allowed_horizontal==True:
                            return[2, 0]
                    if c_board[0][2][1]==False:
                        if self._cells[0][2]._allowed_horizontal==True:
                            return[0, 2]
                    if c_board[2][2][1]==False:
                        if self._cells[2][2]._allowed_horizontal==True:
                            return[2, 2]
                return [1, 1]
        if c_board[0][0]==[True, False] and c_board[2][0]==[False, False] and c_board[0][2]==[False, False] and c_board[2][2]==[False, False]:
            if self.d_board==[[[False, False], [True, True], [False, False]],
                              [[True, True], [False, False], [True, True]],
                              [[False, False], [True, True], [False, False]]]:
                self.d_board[0][0] = [True, True]
                self.d_board[2][2] = [True, True]
            return [2, 2]
        if c_board[0][0]==[False, False] and c_board[2][0]==[True, False] and c_board[0][2]==[False, False] and c_board[2][2]==[False, False]:
            if self.d_board==[[[False, False], [True, True], [False, False]],
                              [[True, True], [False, False], [True, True]],
                              [[False, False], [True, True], [False, False]]]:
                self.d_board[0][2] = [True, True]
                self.d_board[2][0] = [True, True]
            return [0, 2]
        if c_board[0][0]==[False, False] and c_board[2][0]==[False, False] and c_board[0][2]==[True, False] and c_board[2][2]==[False, False]:
            if self.d_board==[[[False, False], [True, True], [False, False]],
                              [[True, True], [False, False], [True, True]],
                              [[False, False], [True, True], [False, False]]]:
                self.d_board[0][2] = [True, True]
                self.d_board[2][0] = [True, True]
            return [2, 0]
        if c_board[0][0]==[False, False] and c_board[2][0]==[False, False] and c_board[0][2]==[False, False] and c_board[2][2]==[True, False]:
            if self.d_board==[[[False, False], [True, True], [False, False]],
                              [[True, True], [False, False], [True, True]],
                              [[False, False], [True, True], [False, False]]]:
                self.d_board[0][0] = [True, True]
                self.d_board[2][2] = [True, True]
            return [0, 0]
        if (c_board[0][0]==[False, False] and c_board[0][2]==[False, False] and c_board[1][1]==[True, False] and
            c_board[2][0]==[False, False] and c_board[2][2]==[False, False]):
            self.d_board[0][0] = [True, True]
            self.d_board[2][2] = [True, True]
            return [0, 0]
        if c_board[0][1]==[True, False] and c_board[2][1]==[False, False]:
            return [2, 1]
        if c_board[2][1]==[True, False] and c_board[0][1]==[False, False]:
            return [0, 1]
        if c_board[1][0]==[True, False] and c_board[1][2]==[False, False]:
            return [1, 2]
        if c_board[1][2]==[True, False] and c_board[1][0]==[False, False]:
            return [1, 0]
        if c_board[0][0]==[True, True] and c_board[2][0]==[False, False] and c_board[0][2]==[False, False] and c_board[2][2]==[True, False]:
            return [2, 2]
        if c_board[0][0]==[False, False] and c_board[2][0]==[True, True] and c_board[0][2]==[True, False] and c_board[2][2]==[False, False]:
            return [0, 2]
        if c_board[0][0]==[False, False] and c_board[2][0]==[True, False] and c_board[0][2]==[True, True] and c_board[2][2]==[False, False]:
            return [2, 0]
        if c_board[0][0]==[True, False] and c_board[2][0]==[False, False] and c_board[0][2]==[False, False] and c_board[2][2]==[True, True]:
            return [0, 0]
        if c_board[0][1]==[True, True] and c_board[2][1]==[True, False]:
            return [2, 1]
        if c_board[2][1]==[True, True] and c_board[0][1]==[True, False]:
            return [0, 1]
        if c_board[1][0]==[True, True] and c_board[1][2]==[True, False]:
            return [1, 2]
        if c_board[1][2]==[True, True] and c_board[1][0]==[True, False]:
            return [1, 0]
        if self.d_board[0][0]==[True, True] and c_board[0][0]==[False, False]:
            return [0, 0]
        if self.d_board[1][0]==[True, True] and c_board[1][0]==[False, False]:
            return [1, 0]
        if self.d_board[2][0]==[True, True] and c_board[2][0]==[False, False]:
            return [2, 0]
        if self.d_board[0][1]==[True, True] and c_board[0][1]==[False, False]:
            return [0, 1]
        if self.d_board[2][1]==[True, True] and c_board[2][1]==[False, False]:
            return [2, 1]
        if self.d_board[0][2]==[True, True] and c_board[0][2]==[False, False]:
            return [0, 2]
        if self.d_board[1][2]==[True, True] and c_board[1][2]==[False, False]:
            return [1, 2]
        if self.d_board[2][2]==[True, True] and c_board[2][2]==[False, False]:
            return [2, 2]
        if self.d_board[0][0]==[True, True] and c_board[0][0]==[True, False]:
            return [0, 0]
        if self.d_board[1][0]==[True, True] and c_board[1][0]==[True, False]:
            return [1, 0]
        if self.d_board[2][0]==[True, True] and c_board[2][0]==[True, False]:
            return [2, 0]
        if self.d_board[0][1]==[True, True] and c_board[0][1]==[True, False]:
            return [0, 1]
        if self.d_board[2][1]==[True, True] and c_board[2][1]==[True, False]:
            return [2, 1]
        if self.d_board[0][2]==[True, True] and c_board[0][2]==[True, False]:
            return [0, 2]
        if self.d_board[1][2]==[True, True] and c_board[1][2]==[True, False]:
            return [1, 2]
        if self.d_board[2][2]==[True, True] and c_board[2][2]==[True, False]:
            return [2, 2]

def make_board(button1, button2, win):
    button1.destroy()
    button2.destroy()
    b1 = Board(100, 100, 150, win)

def make_AI_board(button1, button2, win):
    button1.destroy()
    button2.destroy()
    b1 = AI_Board(100, 100, 150, win)
