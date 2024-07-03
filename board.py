import copy
import tkinter as tk
from cell import Cell
from graphics import Line, Point
import time



class Board():
    def __init__(self, cell_size, x1, y1, win):
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
                self._vertical_score_teller.destroy()
                self._horizontal_score_teller.destroy()
                self.display_scores()
                self.end_buttons()
                return [True, True]
            return [True, False]
        return [False, False]

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
                self._vertical_score_teller.destroy()
                self._horizontal_score_teller.destroy()
                self.display_scores()
                self.end_buttons()

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
        self._vertical_turn = True
        self._vertical_score_teller.destroy()
        self._horizontal_score_teller.destroy()
        self.display_scores()

    def main_menu(self):
        self.close.destroy()
        self.replay.destroy()
        self.menu.destroy()
        self._vertical_score_teller.destroy()
        self._horizontal_score_teller.destroy()
        necesary = tk.StringVar()
        necesary.set('Game Select')
        title = tk.Label(self._win.get_root(), textvariable=necesary)
        title.place(x=1, y=1, width=self._win._width)
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
        button1 = tk.Button(self._win.get_root(), bg="#00C000", activebackground="#009000", text="Tic-Tac-Toe",
                            anchor="center")
        button2 = tk.Button(self._win.get_root(), bg="#00C000", activebackground="#009000", text="Tick-oaT-Two",
                            anchor="center")
        button3 = tk.Button(self._win.get_root(), bg="#00C000", activebackground="#009000", text="Inverse Tic-Tac-Toe",
                            anchor="center")
        button1['command'] = lambda button1=button1, button2=button2, button3=button3, win=self._win: tac([button1, button2, button3], win)
        button2['command'] = lambda button1=button1, button2=button2, button3=button3, win=self._win: oat([button1, button2, button3], win)
        button3['command'] = lambda button1=button1, button2=button2, button3=button3, win=self._win: inv([button1, button2, button3], win)
        button1.place(x=window_length/9, y=window_height/5, width=window_length/3, height=window_height/5)
        button2.place(x=window_length/9, y=(window_height/5)*3, width=window_length/3, height=window_height/5)
        button3.place(x=5*(window_length/9), y=(window_height/5), width=window_length/3, height=window_height/5)

    def display_scores(self):
        vertical_score = tk.StringVar()
        vertical_score.set(f"Vertical wins: {self._vertical_score}")
        self._vertical_score_teller = tk.Label(height=1, width=100, bg="#00FF00", fg="black",
                                               textvariable=vertical_score)
        horizontal_score = tk.StringVar()
        horizontal_score.set(f"Horizontal wins: {self._horizontal_score}")
        self._horizontal_score_teller = tk.Label(height=1, width=100, bg="#00FF00", fg="black",
                                                 textvariable=horizontal_score)
        self._vertical_score_teller.place(x=0, y=20, height=20, width=self._win._width)
        self._horizontal_score_teller.place(x=0, y=40, height=20, width=self._win._width)

class AI_Board(Board):
    def __init__(self, cell_size, x1, y1, win):
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
        if move[0] == True:
            if move[1] != True:
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

class RBoard(Board):
    def __init__(self, cell_size, x1, y1, win):
        self._dimensions = 3
        self._cell_size = cell_size
        self._x1 = x1
        self._y1 = y1
        self._win = win
        self._cells = []
        self._buttons = []
        self._x_turn = True
        self.start = "x"
        self._x_score = 0
        self._o_score = 0
        self.close = None
        self.replay = None
        self.menu = None
        self.win_lines = []
        self._x_score_teller = None
        self._o_score_teller = None
        self.display_scores()
        self._create_cells_and_buttons()

    def display_scores(self):
        vertical_score = tk.StringVar()
        vertical_score.set(f"X wins: {self._x_score}")
        self._x_score_teller = tk.Label(height=1, width=100, bg="#00FF00", fg="black",
                                               textvariable=vertical_score)
        horizontal_score = tk.StringVar()
        horizontal_score.set(f"O wins: {self._o_score}")
        self._o_score_teller = tk.Label(height=1, width=100, bg="#00FF00", fg="black",
                                                 textvariable=horizontal_score)
        self._x_score_teller.place(x=0, y=20, height=20, width=self._win._width)
        self._o_score_teller.place(x=0, y=40, height=20, width=self._win._width)

    def move(self, i, j):
        cell = self._cells[i][j]
        if self._x_turn:
            self.x_move(cell, i, j)
        else:
            self.o_move(cell, i, j)

    def x_move(self, cell, i, j):
        if not cell.has_o and not cell.has_x:
            self._cells[i][j].draw_x()
            self._cells[i][j].has_x = True
            self._x_turn = False
            win = self.check_win()
            if win != 0:
                if win == 1:
                    print("X wins!")
                else:
                    print(f"X wins with {win} lines!")
                for col in self._buttons:
                    for button in col:
                        button["state"] = "disabled"
                self._x_score += 1
                self._x_score_teller.destroy()
                self._o_score_teller.destroy()
                self.display_scores()
                self.end_buttons()
                return [True, True]
            else:
                empty_cells = 0
                for col in self._cells:
                    for cell in col:
                        if not cell.has_x and not cell.has_o:
                            empty_cells += 1
                if empty_cells == 0:
                    print("It's a draw!")
                    for col in self._buttons:
                        for button in col:
                            button["state"] = "disabled"
                    self.end_buttons()
                    return [True, True]
            return [True, False]
        return [False, False]

    def o_move(self, cell, i, j):
        if not cell.has_o and not cell.has_x:
            self._cells[i][j].draw_o()
            self._cells[i][j].has_o = True
            self._x_turn = True
            win = self.check_win()
            if win != 0:
                if win == 1:
                    print("O wins!")
                else:
                    print(f"O wins with {win} lines!")
                for col in self._buttons:
                    for button in col:
                        button["state"] = "disabled"
                self._o_score += 1
                self._x_score_teller.destroy()
                self._o_score_teller.destroy()
                self.display_scores()
                self.end_buttons()
            else:
                empty_cells = 0
                for col in self._cells:
                    for cell in col:
                        if not cell.has_x and not cell.has_o:
                            empty_cells += 1
                if empty_cells == 0:
                    print("It's a draw!")
                    for col in self._buttons:
                        for button in col:
                            button["state"] = "disabled"
                    self.end_buttons()

    def check_win(self):
        win_count = 0
        for i in range(0, self._dimensions):
            if ((self._cells[i][0].has_o==True and self._cells[i][1].has_o==True and self._cells[i][2].has_o==True) or
                (self._cells[i][0].has_x==True and self._cells[i][1].has_x==True and self._cells[i][2].has_x==True)):
                win_count += 1
                self._win.draw_line(Line(Point(self._cells[i][0]._x1+self._cell_size/2, self._cells[i][0]._y1),
                                         Point(self._cells[i][0]._x1+self._cell_size/2, self._cells[i][2]._y2)))
                self.win_lines.append(Line(Point(self._cells[i][0]._x1+self._cell_size/2, self._cells[i][0]._y1),
                                           Point(self._cells[i][0]._x1+self._cell_size/2, self._cells[i][2]._y2)))
        for i in range(0, self._dimensions):
            if ((self._cells[0][i].has_o==True and self._cells[1][i].has_o==True and self._cells[2][i].has_o==True) or
                (self._cells[0][i].has_x==True and self._cells[1][i].has_x==True and self._cells[2][i].has_x==True)):
                win_count += 1
                self._win.draw_line(Line(Point(self._cells[0][i]._x1, self._cells[0][i]._y1+self._cell_size/2),
                                         Point(self._cells[2][i]._x2, self._cells[0][i]._y1+self._cell_size/2)))
                self.win_lines.append(Line(Point(self._cells[0][i]._x1, self._cells[0][i]._y1+self._cell_size/2),
                                           Point(self._cells[2][i]._x2, self._cells[0][i]._y1+self._cell_size/2)))
        if ((self._cells[0][0].has_o==True and self._cells[1][1].has_o==True and self._cells[2][2].has_o==True) or
            (self._cells[0][0].has_x==True and self._cells[1][1].has_x==True and self._cells[2][2].has_x==True)):
            win_count += 1
            self._win.draw_line(Line(Point(self._cells[0][0]._x1, self._cells[0][0]._y1),
                                     Point(self._cells[2][2]._x2, self._cells[2][2]._y2)))
            self.win_lines.append(Line(Point(self._cells[0][0]._x1, self._cells[0][0]._y1),
                                       Point(self._cells[2][2]._x2, self._cells[2][2]._y2)))
        if ((self._cells[0][2].has_o==True and self._cells[1][1].has_o==True and self._cells[2][0].has_o==True) or
            (self._cells[0][2].has_x==True and self._cells[1][1].has_x==True and self._cells[2][0].has_x==True)):
            win_count += 1
            self._win.draw_line(Line(Point(self._cells[2][0]._x2, self._cells[2][0]._y1),
                                     Point(self._cells[0][2]._x1, self._cells[0][2]._y2)))
            self.win_lines.append(Line(Point(self._cells[2][0]._x2, self._cells[2][0]._y1),
                                       Point(self._cells[0][2]._x1, self._cells[0][2]._y2)))
        return win_count

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
        if self.start == "o":
            self._x_turn = True
            self.start = "x"
        else:
            self._x_turn = False
            self.start = "o"

    def main_menu(self):
        self.close.destroy()
        self.replay.destroy()
        self.menu.destroy()
        self._x_score_teller.destroy()
        self._o_score_teller.destroy()
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
        necesary = tk.StringVar()
        necesary.set('Game Select')
        title = tk.Label(self._win.get_root(), textvariable=necesary)
        title.place(x=1, y=1, width=self._win._width)
        button1 = tk.Button(self._win.get_root(), bg="#00C000", activebackground="#009000", text="Tic-Tac-Toe",
                            anchor="center")
        button2 = tk.Button(self._win.get_root(), bg="#00C000", activebackground="#009000", text="Tick-oaT-Two",
                            anchor="center")
        button3 = tk.Button(self._win.get_root(), bg="#00C000", activebackground="#009000", text="Inverse Tic-Tac-Toe",
                            anchor="center")
        button1['command'] = lambda button1=button1, button2=button2, button3=button3, win=self._win: tac([button1, button2, button3], win)
        button2['command'] = lambda button1=button1, button2=button2, button3=button3, win=self._win: oat([button1, button2, button3], win)
        button3['command'] = lambda button1=button1, button2=button2, button3=button3, win=self._win: inv([button1, button2, button3], win)
        button1.place(x=window_length/9, y=window_height/5, width=window_length/3, height=window_height/5)
        button2.place(x=window_length/9, y=(window_height/5)*3, width=window_length/3, height=window_height/5)
        button3.place(x=5*(window_length/9), y=(window_height/5), width=window_length/3, height=window_height/5)

class AI_RBoard(RBoard):
    def reset_board(self):
        super().reset_board()
        if self._x_turn == False:
            self.o_move(self._cells[0][0], 0, 0)

    def move(self, i, j):
        cell = self._cells[i][j]
        if self._x_turn:
            move = self.x_move(cell, i, j)
        if move[0] == True:
            if move[1] != True:
                self._win.redraw()
                time.sleep(1)
                AI_move = self.best_move()
                if AI_move != None and not self._x_turn:
                    self.o_move(self._cells[AI_move[0]][AI_move[1]], AI_move[0], AI_move[1])
                self._x_turn = True

    def best_move(self):
        c_board = []
        for col in self._cells:
            c_col = []
            for cell in col:
                if cell.has_x:
                    c_col.append('x')
                elif cell.has_o:
                    c_col.append('o')
                else:
                    c_col.append(None)
            c_board.append(c_col)
        win_lines = []
        for i in range(0, self._dimensions):
            if ((self._cells[i][0].has_o==True and self._cells[i][1].has_o==True) or
                (self._cells[i][0].has_o==True and self._cells[i][2].has_o==True) or
                (self._cells[i][1].has_o==True and self._cells[i][2].has_o==True)):
                win_lines.append([[i, 0], [i, 1], [i, 2]])
        for i in range(0, self._dimensions):
            if ((self._cells[0][i].has_o==True and self._cells[1][i].has_o==True) or
                (self._cells[0][i].has_o==True and self._cells[2][i].has_o==True) or
                (self._cells[1][i].has_o==True and self._cells[2][i].has_o==True)):
                win_lines.append([[0, i], [1, i], [2, i]])
        if ((self._cells[0][0].has_o==True and self._cells[1][1].has_o==True) or
            (self._cells[0][0].has_o==True and self._cells[2][2].has_o==True) or
            (self._cells[1][1].has_o==True and self._cells[2][2].has_o==True)):
            win_lines.append([[0, 0], [1, 1], [2, 2]])
        if ((self._cells[0][2].has_o==True and self._cells[1][1].has_o==True) or
            (self._cells[0][2].has_o==True and self._cells[2][0].has_o==True) or
            (self._cells[1][1].has_o==True and self._cells[2][0].has_o==True)):
            win_lines.append([[0, 2], [1, 1], [2, 0]])
        if win_lines != []:
            for line in win_lines:
                for cell in line:
                    if not self._cells[cell[0]][cell[1]].has_o and not self._cells[cell[0]][cell[1]].has_x:
                        return cell
        lose_lines = []
        for i in range(0, self._dimensions):
            if ((self._cells[i][0].has_x==True and self._cells[i][1].has_x==True) or
                (self._cells[i][0].has_x==True and self._cells[i][2].has_x==True) or
                (self._cells[i][1].has_x==True and self._cells[i][2].has_x==True)):
                lose_lines.append([[i, 0], [i, 1], [i, 2]])
        for i in range(0, self._dimensions):
            if ((self._cells[0][i].has_x==True and self._cells[1][i].has_x==True) or
                (self._cells[0][i].has_x==True and self._cells[2][i].has_x==True) or
                (self._cells[1][i].has_x==True and self._cells[2][i].has_x==True)):
                lose_lines.append([[0, i], [1, i], [2, i]])
        if ((self._cells[0][0].has_x==True and self._cells[1][1].has_x==True) or
            (self._cells[0][0].has_x==True and self._cells[2][2].has_x==True) or
            (self._cells[1][1].has_x==True and self._cells[2][2].has_x==True)):
            lose_lines.append([[0, 0], [1, 1], [2, 2]])
        if ((self._cells[0][2].has_x==True and self._cells[1][1].has_x==True) or
            (self._cells[0][2].has_x==True and self._cells[2][0].has_x==True) or
            (self._cells[1][1].has_x==True and self._cells[2][0].has_x==True)):
            lose_lines.append([[0, 2], [1, 1], [2, 0]])
        if lose_lines != []:
            for line in lose_lines:
                for cell in line:
                    if not self._cells[cell[0]][cell[1]].has_o and not self._cells[cell[0]][cell[1]].has_x:
                        return cell
        if c_board == [['o', None, None],
                       [None, 'x', None],
                       [None, None, None]]:
            return [2, 2]
        if c_board == [['x', None, None],
                       [None, None, None],
                       [None, None, None]]:
            return [1, 1]
        if c_board == [[None, None, 'x'],
                       [None, None, None],
                       [None, None, None]]:
            return [1, 1]
        if c_board == [[None, None, None],
                       [None, None, None],
                       ['x', None, None]]:
            return [1, 1]
        if c_board == [[None, None, None],
                       [None, None, None],
                       [None, None, 'x']]:
            return [1, 1]
        if c_board == [['x', None, None],
                       [None, 'o', None],
                       [None, None, 'x']]:
            return [1, 0]
        if c_board == [[None, None, 'x'],
                       [None, 'o', None],
                       ['x', None, None]]:
            return [1, 0]
        two_list = []
        for i in range(0, 3):
            two_col = []
            for j in range(0, 3):
                twos = 0
                if c_board[i][j] == None:
                    if ((i == 1 and (j == 0 or j == 2)) or
                        (j == 1 and (i == 0 or i == 2))):
                        twos += self.wcheck_edge(i, j)
                    elif i == 1 and j == 1:
                        twos += self.wcheck_center()
                    else:
                        twos += self.wcheck_corner(i, j)
                two_col.append(twos)
            two_list.append(two_col)
        best = 0
        for i in range(0, 2):
            for j in range(0, 2):
                if best < two_list[i][j]:
                    best = two_list[i][j]
                    good_i = i
                    good_j = j
        if best != 0:
            return [good_i, good_j]
        two_list = []
        for i in range(0, 3):
            two_col = []
            for j in range(0, 3):
                twos = 0
                if c_board[i][j] == None:
                    if ((i == 1 and (j == 0 or j == 2)) or
                        (j == 1 and (i == 0 or i == 2))):
                        twos += self.lcheck_edge(i, j)
                    elif i == 1 and j == 1:
                        twos += self.lcheck_center()
                    else:
                        twos += self.lcheck_corner(i, j)
                two_col.append(twos)
            two_list.append(two_col)
        best = 0
        for i in range(0, 2):
            for j in range(0, 2):
                if best < two_list[i][j]:
                    best = two_list[i][j]
                    good_i = i
                    good_j = j
        if best != 0:
            return [good_i, good_j]
        if c_board[1][1] == None:
            return [1, 1]
        if c_board[1][0] == None:
            return [1, 0]
        if c_board[1][2] == None:
            return [1, 2]
        if c_board[0][1] == None:
            return [0, 1]
        if c_board[0][2] == None:
            return [2, 1]
        if c_board[2][0] == None:
            return [2, 0]
        if c_board[0][2] == None:
            return [0, 2]
        if c_board[0][0] == None:
            return [0, 0]
        if c_board[2][2] == None:
            return [2, 2]
        return None

    def wcheck_edge(self, i, j):
        twos = 0
        if i == 1 and j == 0:
            if (self._cells[0][0].has_o and not self._cells[2][0].has_x) or (not self._cells[0][0].has_x and self._cells[2][0].has_o):
                twos += 1
            if (self._cells[1][2].has_o and not self._cells[1][1].has_x) or (not self._cells[1][2].has_x and self._cells[1][1].has_o):
                twos += 1
        if i == 1 and j == 2:
            if (self._cells[0][2].has_o and not self._cells[2][2].has_x) or (not self._cells[0][2].has_x and self._cells[2][2].has_o):
                twos += 1
            if (self._cells[1][0].has_o and not self._cells[1][1].has_x) or (not self._cells[1][0].has_x and self._cells[1][1].has_o):
                twos += 1
        if i == 0 and j == 1:
            if (self._cells[0][0].has_o and not self._cells[0][2].has_x) or (not self._cells[0][0].has_x and self._cells[0][2].has_o):
                twos += 1
            if (self._cells[2][1].has_o and not self._cells[1][1].has_x) or (not self._cells[2][1].has_x and self._cells[1][1].has_o):
                twos += 1
        if i == 2 and j == 1:
            if (self._cells[2][0].has_o and not self._cells[2][2].has_x) or (not self._cells[2][0].has_x and self._cells[2][2].has_o):
                twos += 1
            if (self._cells[0][1].has_o and not self._cells[1][1].has_x) or (not self._cells[0][1].has_x and self._cells[1][1].has_o):
                twos += 1
        return twos

    def lcheck_edge(self, i, j):
        twos = 0
        if i == 1 and j == 0:
            if (self._cells[0][0].has_x and not self._cells[2][0].has_o) or (not self._cells[0][0].has_o and self._cells[2][0].has_x):
                twos += 1
            if (self._cells[1][2].has_x and not self._cells[1][1].has_o) or (not self._cells[1][2].has_o and self._cells[1][1].has_x):
                twos += 1
        if i == 1 and j == 2:
            if (self._cells[0][2].has_x and not self._cells[2][2].has_o) or (not self._cells[0][2].has_o and self._cells[2][2].has_x):
                twos += 1
            if (self._cells[1][0].has_x and not self._cells[1][1].has_o) or (not self._cells[1][0].has_o and self._cells[1][1].has_x):
                twos += 1
        if i == 0 and j == 1:
            if (self._cells[0][0].has_x and not self._cells[0][2].has_o) or (not self._cells[0][0].has_o and self._cells[0][2].has_x):
                twos += 1
            if (self._cells[2][1].has_x and not self._cells[1][1].has_o) or (not self._cells[2][1].has_o and self._cells[1][1].has_x):
                twos += 1
        if i == 2 and j == 1:
            if (self._cells[2][0].has_x and not self._cells[2][2].has_o) or (not self._cells[2][0].has_o and self._cells[2][2].has_x):
                twos += 1
            if (self._cells[0][1].has_x and not self._cells[1][1].has_o) or (not self._cells[0][1].has_o and self._cells[1][1].has_x):
                twos += 1
        return twos

    def wcheck_corner(self, i, j):
        twos = 0
        if i == 0 and j == 0:
            if (self._cells[0][1].has_o and not self._cells[0][2].has_x) or (not self._cells[0][1].has_x and self._cells[0][2].has_o):
                twos += 1
            if (self._cells[1][0].has_o and not self._cells[2][0].has_x) or (not self._cells[1][0].has_x and self._cells[2][0].has_o):
                twos += 1
            if (self._cells[1][1].has_o and not self._cells[2][2].has_x) or (not self._cells[1][1].has_x and self._cells[2][2].has_o):
                twos += 1
        if i == 2 and j == 2:
            if (self._cells[2][1].has_o and not self._cells[2][0].has_x) or (not self._cells[2][1].has_x and self._cells[2][0].has_o):
                twos += 1
            if (self._cells[1][2].has_o and not self._cells[0][2].has_x) or (not self._cells[1][2].has_x and self._cells[0][2].has_o):
                twos += 1
            if (self._cells[1][1].has_o and not self._cells[0][0].has_x) or (not self._cells[1][1].has_x and self._cells[0][0].has_o):
                twos += 1
        if i == 0 and j == 2:
            if (self._cells[0][1].has_o and not self._cells[0][0].has_x) or (not self._cells[0][1].has_x and self._cells[0][0].has_o):
                twos += 1
            if (self._cells[1][2].has_o and not self._cells[2][2].has_x) or (not self._cells[1][2].has_x and self._cells[2][2].has_o):
                twos += 1
            if (self._cells[1][1].has_o and not self._cells[2][0].has_x) or (not self._cells[1][1].has_x and self._cells[2][0].has_o):
                twos += 1
        if i == 2 and j == 0:
            if (self._cells[2][1].has_o and not self._cells[2][2].has_x) or (not self._cells[2][1].has_x and self._cells[2][2].has_o):
                twos += 1
            if (self._cells[1][0].has_o and not self._cells[0][0].has_x) or (not self._cells[1][0].has_x and self._cells[0][0].has_o):
                twos += 1
            if (self._cells[1][1].has_o and not self._cells[0][2].has_x) or (not self._cells[1][1].has_x and self._cells[0][2].has_o):
                twos += 1
        return twos

    def lcheck_corner(self, i, j):
        twos = 0
        if i == 0 and j == 0:
            if (self._cells[0][1].has_x and not self._cells[0][2].has_o) or (not self._cells[0][1].has_o and self._cells[0][2].has_x):
                twos += 1
            if (self._cells[1][0].has_x and not self._cells[2][0].has_o) or (not self._cells[1][0].has_o and self._cells[2][0].has_x):
                twos += 1
            if (self._cells[1][1].has_x and not self._cells[2][2].has_o) or (not self._cells[1][1].has_o and self._cells[2][2].has_x):
                twos += 1
        if i == 2 and j == 2:
            if (self._cells[2][1].has_x and not self._cells[2][0].has_o) or (not self._cells[2][1].has_o and self._cells[2][0].has_x):
                twos += 1
            if (self._cells[1][2].has_x and not self._cells[0][2].has_o) or (not self._cells[1][2].has_o and self._cells[0][2].has_x):
                twos += 1
            if (self._cells[1][1].has_x and not self._cells[0][0].has_o) or (not self._cells[1][1].has_o and self._cells[0][0].has_x):
                twos += 1
        if i == 0 and j == 2:
            if (self._cells[0][1].has_x and not self._cells[0][0].has_o) or (not self._cells[0][1].has_o and self._cells[0][0].has_x):
                twos += 1
            if (self._cells[1][2].has_x and not self._cells[2][2].has_o) or (not self._cells[1][2].has_o and self._cells[2][2].has_x):
                twos += 1
            if (self._cells[1][1].has_x and not self._cells[2][0].has_o) or (not self._cells[1][1].has_o and self._cells[2][0].has_x):
                twos += 1
        if i == 2 and j == 0:
            if (self._cells[2][1].has_x and not self._cells[2][2].has_o) or (not self._cells[2][1].has_o and self._cells[2][2].has_x):
                twos += 1
            if (self._cells[1][0].has_x and not self._cells[0][0].has_o) or (not self._cells[1][0].has_o and self._cells[0][0].has_x):
                twos += 1
            if (self._cells[1][1].has_x and not self._cells[0][2].has_o) or (not self._cells[1][1].has_o and self._cells[0][2].has_x):
                twos += 1
        return twos

    def wcheck_center(self):
        twos = 0
        if (self._cells[0][2].has_o and not self._cells[2][0].has_x) or (self._cells[2][0].has_o and not self._cells[0][2].has_x):
            twos += 1
        if (self._cells[2][2].has_o and not self._cells[0][0].has_x) or (self._cells[0][0].has_o and not self._cells[2][2].has_x):
            twos += 1
        if (self._cells[0][1].has_o and not self._cells[2][1].has_x) or (self._cells[2][1].has_o and not self._cells[0][1].has_x):
            twos += 1
        if (self._cells[1][2].has_o and not self._cells[1][0].has_x) or (self._cells[1][0].has_o and not self._cells[1][2].has_x):
            twos += 1
        return twos

    def lcheck_center(self):
        twos = 0
        if (self._cells[0][2].has_x and not self._cells[2][0].has_o) or (self._cells[2][0].has_x and not self._cells[0][2].has_o):
            twos += 1
        if (self._cells[2][2].has_x and not self._cells[0][0].has_o) or (self._cells[0][0].has_x and not self._cells[2][2].has_o):
            twos += 1
        if (self._cells[0][1].has_x and not self._cells[2][1].has_o) or (self._cells[2][1].has_x and not self._cells[0][1].has_o):
            twos += 1
        if (self._cells[1][2].has_x and not self._cells[1][0].has_o) or (self._cells[1][0].has_x and not self._cells[1][2].has_o):
            twos += 1
        return twos

class IBoard(RBoard):
    def o_move(self, cell, i, j):
        if not cell.has_o and not cell.has_x:
            self._cells[i][j].draw_o()
            self._cells[i][j].has_o = True
            self._x_turn = True
            win = self.check_win()
            if win != 0:
                if win == 1:
                    print("O loses!")
                else:
                    print(f"O loses with {win} lines!")
                for col in self._buttons:
                    for button in col:
                        button["state"] = "disabled"
                self._x_score += 1
                self._x_score_teller.destroy()
                self._o_score_teller.destroy()
                self.display_scores()
                self.end_buttons()
            else:
                empty_cells = 0
                for col in self._cells:
                    for cell in col:
                        if not cell.has_x and not cell.has_o:
                            empty_cells += 1
                if empty_cells == 0:
                    print("It's a draw!")
                    for col in self._buttons:
                        for button in col:
                            button["state"] = "disabled"
                    self.end_buttons()

    def x_move(self, cell, i, j):
        if not cell.has_o and not cell.has_x:
            self._cells[i][j].draw_x()
            self._cells[i][j].has_x = True
            self._x_turn = False
            win = self.check_win()
            if win != 0:
                if win == 1:
                    print("X loses!")
                else:
                    print(f"X loses with {win} lines!")
                for col in self._buttons:
                    for button in col:
                        button["state"] = "disabled"
                self._o_score += 1
                self._x_score_teller.destroy()
                self._o_score_teller.destroy()
                self.display_scores()
                self.end_buttons()
                return [True, True]
            else:
                empty_cells = 0
                for col in self._cells:
                    for cell in col:
                        if not cell.has_x and not cell.has_o:
                            empty_cells += 1
                if empty_cells == 0:
                    print("It's a draw!")
                    for col in self._buttons:
                        for button in col:
                            button["state"] = "disabled"
                    self.end_buttons()
                    return [True, True]
            return [True, False]
        return [False, False]

class AI_IBoard(IBoard):
    def reset_board(self):
        super().reset_board()
        if self._x_turn == False:
            self.o_move(self._cells[1][1], 1, 1)

    def move(self, i, j):
        cell = self._cells[i][j]
        if self._x_turn:
            move = self.x_move(cell, i, j)
        if move[0] == True:
            if move[1] != True:
                self._win.redraw()
                time.sleep(1)
                AI_move = self.best_move()
                if AI_move != None and not self._x_turn:
                    self.o_move(self._cells[AI_move[0]][AI_move[1]], AI_move[0], AI_move[1])
                self._x_turn = True

    def best_move(self):
        c_board = []
        for col in self._cells:
            c_col = []
            for cell in col:
                if cell.has_x:
                    c_col.append('x')
                elif cell.has_o:
                    c_col.append('o')
                else:
                    c_col.append(None)
            c_board.append(c_col)
        available_cells = []
        for i in range(0, 3):
            a_col = []
            for j in range(0, 3):
                if c_board[i][j] == None:
                    a_col.append(True)
                    continue
                a_col.append(False)
            available_cells.append(a_col)
        if len(available_cells) == 1:
            return available_cells[0]
        win_lines = []
        for i in range(0, self._dimensions):
            if ((self._cells[i][0].has_o==True and self._cells[i][1].has_o==True) or
                (self._cells[i][0].has_o==True and self._cells[i][2].has_o==True) or
                (self._cells[i][1].has_o==True and self._cells[i][2].has_o==True)):
                win_lines.append([[i, 0], [i, 1], [i, 2]])
        for i in range(0, self._dimensions):
            if ((self._cells[0][i].has_o==True and self._cells[1][i].has_o==True) or
                (self._cells[0][i].has_o==True and self._cells[2][i].has_o==True) or
                (self._cells[1][i].has_o==True and self._cells[2][i].has_o==True)):
                win_lines.append([[0, i], [1, i], [2, i]])
        if ((self._cells[0][0].has_o==True and self._cells[1][1].has_o==True) or
            (self._cells[0][0].has_o==True and self._cells[2][2].has_o==True) or
            (self._cells[1][1].has_o==True and self._cells[2][2].has_o==True)):
            win_lines.append([[0, 0], [1, 1], [2, 2]])
        if ((self._cells[0][2].has_o==True and self._cells[1][1].has_o==True) or
            (self._cells[0][2].has_o==True and self._cells[2][0].has_o==True) or
            (self._cells[1][1].has_o==True and self._cells[2][0].has_o==True)):
            win_lines.append([[0, 2], [1, 1], [2, 0]])
        if win_lines != []:
            for line in win_lines:
                for cell in line:
                    if available_cells[cell[0]][cell[1]] == True:
                        available_cells[cell[0]][cell[1]] = False
        o_three = copy.deepcopy(available_cells)
        pos = 0
        for a_col in available_cells:
            for a_cell in a_col:
                if a_cell == True:
                    pos += 1
        if pos == 1:
            for i in range(0, 2):
                for j in range(0, 2):
                    if available_cells[i][j] == True:
                        return [i, j]
        if o_three == [[False, False, False], [False, False, False], [False, False, False]]:
            for i in range(0, 3):
                for j in range(0, 3):
                    if c_board[i][j] == None:
                        return [i, j]
        lose_lines = []
        for i in range(0, self._dimensions):
            if ((self._cells[i][0].has_x==True and self._cells[i][1].has_x==True) or
                (self._cells[i][0].has_x==True and self._cells[i][2].has_x==True) or
                (self._cells[i][1].has_x==True and self._cells[i][2].has_x==True)):
                lose_lines.append([[i, 0], [i, 1], [i, 2]])
        for i in range(0, self._dimensions):
            if ((self._cells[0][i].has_x==True and self._cells[1][i].has_x==True) or
                (self._cells[0][i].has_x==True and self._cells[2][i].has_x==True) or
                (self._cells[1][i].has_x==True and self._cells[2][i].has_x==True)):
                lose_lines.append([[0, i], [1, i], [2, i]])
        if ((self._cells[0][0].has_x==True and self._cells[1][1].has_x==True) or
            (self._cells[0][0].has_x==True and self._cells[2][2].has_x==True) or
            (self._cells[1][1].has_x==True and self._cells[2][2].has_x==True)):
            lose_lines.append([[0, 0], [1, 1], [2, 2]])
        if ((self._cells[0][2].has_x==True and self._cells[1][1].has_x==True) or
            (self._cells[0][2].has_x==True and self._cells[2][0].has_x==True) or
            (self._cells[1][1].has_x==True and self._cells[2][0].has_x==True)):
            lose_lines.append([[0, 2], [1, 1], [2, 0]])
        if lose_lines != []:
            for line in lose_lines:
                for cell in line:
                    if available_cells[cell[0]][cell[1]] == True:
                        available_cells[cell[0]][cell[1]] = False
        x_block = copy.deepcopy(available_cells)
        pos = 0
        for a_col in available_cells:
            for a_cell in a_col:
                if a_cell == True:
                    pos += 1
        if pos == 1:
            for i in range(0, 2):
                for j in range(0, 2):
                    if available_cells[i][j] == True:
                        return [i, j]
        if x_block == [[False, False, False], [False, False, False], [False, False, False]]:
            available_cells = copy.deepcopy(o_three)
            x_block = copy.deepcopy(o_three)
        two_list = []
        for i in range(0, 3):
            two_col = []
            for j in range(0, 3):
                twos = None
                if available_cells[i][j] == True:
                    if ((i == 1 and (j == 0 or j == 2)) or
                        (j == 1 and (i == 0 or i == 2))):
                        twos = self.wcheck_edge(i, j)
                    elif i == 1 and j == 1:
                        twos = self.wcheck_center()
                    else:
                        twos = self.wcheck_corner(i, j)
                two_col.append(twos)
            two_list.append(two_col)
        min_list = self.min_list(two_list)
        for i in range(0, 3):
            for j in range(0, 3):
                if min_list[i][j] == None:
                    available_cells[i][j] = False
        o_twos = copy.deepcopy(available_cells)
        pos = 0
        for a_col in available_cells:
            for a_cell in a_col:
                if a_cell == True:
                    pos += 1
        if pos == 1:
            for i in range(0, 2):
                for j in range(0, 2):
                    if available_cells[i][j] == True:
                        return [i, j]
        if o_twos == [[False, False, False], [False, False, False], [False, False, False]]:
            available_cells = copy.deepcopy(x_block)
            o_twos = copy.deepcopy(x_block)
        two_list = []
        for i in range(0, 3):
            two_col = []
            for j in range(0, 3):
                twos = None
                if available_cells[i][j] == True:
                    if ((i == 1 and (j == 0 or j == 2)) or
                        (j == 1 and (i == 0 or i == 2))):
                        twos = self.lcheck_edge(i, j)
                    elif i == 1 and j == 1:
                        twos = self.lcheck_center()
                    else:
                        twos = self.lcheck_corner(i, j)
                two_col.append(twos)
            two_list.append(two_col)
        min_list = self.min_list(two_list)
        for i in range(0, 3):
            for j in range(0, 3):
                if min_list[i][j] == None:
                    available_cells[i][j] = False
        x_twos = copy.deepcopy(available_cells)
        pos = 0
        for a_col in available_cells:
            for a_cell in a_col:
                if a_cell == True:
                    pos += 1
        if pos == 1:
            for i in range(0, 2):
                for j in range(0, 2):
                    if available_cells[i][j] == True:
                        return [i, j]
        if x_twos == [[False, False, False], [False, False, False], [False, False, False]]:
            available_cells = copy.deepcopy(o_twos)
        for i in range (0, 3):
            for j in range (0, 3):
                if available_cells[i][j] == True:
                    return [i, j]

    def min_list(self, l):
        min_list = []
        min = float("inf")
        for c in l:
            for num in c:
                if num != None:
                    if num < min:
                        min = num
        for c in l:
            min_col = []
            for num in c:
                if num == None:
                    min_col.append(num)
                elif num == min:
                    min_col.append(num)
                elif num > min:
                    min_col.append(None)
            min_list.append(min_col)
        return min_list

    def wcheck_edge(self, i, j):
        twos = 0
        if i == 1 and j == 0:
            if (self._cells[0][0].has_o and not self._cells[2][0].has_x) or (not self._cells[0][0].has_x and self._cells[2][0].has_o):
                twos += 1
            if (self._cells[1][2].has_o and not self._cells[1][1].has_x) or (not self._cells[1][2].has_x and self._cells[1][1].has_o):
                twos += 1
        if i == 1 and j == 2:
            if (self._cells[0][2].has_o and not self._cells[2][2].has_x) or (not self._cells[0][2].has_x and self._cells[2][2].has_o):
                twos += 1
            if (self._cells[1][0].has_o and not self._cells[1][1].has_x) or (not self._cells[1][0].has_x and self._cells[1][1].has_o):
                twos += 1
        if i == 0 and j == 1:
            if (self._cells[0][0].has_o and not self._cells[0][2].has_x) or (not self._cells[0][0].has_x and self._cells[0][2].has_o):
                twos += 1
            if (self._cells[2][1].has_o and not self._cells[1][1].has_x) or (not self._cells[2][1].has_x and self._cells[1][1].has_o):
                twos += 1
        if i == 2 and j == 1:
            if (self._cells[2][0].has_o and not self._cells[2][2].has_x) or (not self._cells[2][0].has_x and self._cells[2][2].has_o):
                twos += 1
            if (self._cells[0][1].has_o and not self._cells[1][1].has_x) or (not self._cells[0][1].has_x and self._cells[1][1].has_o):
                twos += 1
        return twos

    def lcheck_edge(self, i, j):
        twos = 0
        if i == 1 and j == 0:
            if (self._cells[0][0].has_x and not self._cells[2][0].has_o) or (not self._cells[0][0].has_o and self._cells[2][0].has_x):
                twos += 1
            if (self._cells[1][2].has_x and not self._cells[1][1].has_o) or (not self._cells[1][2].has_o and self._cells[1][1].has_x):
                twos += 1
        if i == 1 and j == 2:
            if (self._cells[0][2].has_x and not self._cells[2][2].has_o) or (not self._cells[0][2].has_o and self._cells[2][2].has_x):
                twos += 1
            if (self._cells[1][0].has_x and not self._cells[1][1].has_o) or (not self._cells[1][0].has_o and self._cells[1][1].has_x):
                twos += 1
        if i == 0 and j == 1:
            if (self._cells[0][0].has_x and not self._cells[0][2].has_o) or (not self._cells[0][0].has_o and self._cells[0][2].has_x):
                twos += 1
            if (self._cells[2][1].has_x and not self._cells[1][1].has_o) or (not self._cells[2][1].has_o and self._cells[1][1].has_x):
                twos += 1
        if i == 2 and j == 1:
            if (self._cells[2][0].has_x and not self._cells[2][2].has_o) or (not self._cells[2][0].has_o and self._cells[2][2].has_x):
                twos += 1
            if (self._cells[0][1].has_x and not self._cells[1][1].has_o) or (not self._cells[0][1].has_o and self._cells[1][1].has_x):
                twos += 1
        return twos

    def wcheck_corner(self, i, j):
        twos = 0
        if i == 0 and j == 0:
            if (self._cells[0][1].has_o and not self._cells[0][2].has_x) or (not self._cells[0][1].has_x and self._cells[0][2].has_o):
                twos += 1
            if (self._cells[1][0].has_o and not self._cells[2][0].has_x) or (not self._cells[1][0].has_x and self._cells[2][0].has_o):
                twos += 1
            if (self._cells[1][1].has_o and not self._cells[2][2].has_x) or (not self._cells[1][1].has_x and self._cells[2][2].has_o):
                twos += 1
        if i == 2 and j == 2:
            if (self._cells[2][1].has_o and not self._cells[2][0].has_x) or (not self._cells[2][1].has_x and self._cells[2][0].has_o):
                twos += 1
            if (self._cells[1][2].has_o and not self._cells[0][2].has_x) or (not self._cells[1][2].has_x and self._cells[0][2].has_o):
                twos += 1
            if (self._cells[1][1].has_o and not self._cells[0][0].has_x) or (not self._cells[1][1].has_x and self._cells[0][0].has_o):
                twos += 1
        if i == 0 and j == 2:
            if (self._cells[0][1].has_o and not self._cells[0][0].has_x) or (not self._cells[0][1].has_x and self._cells[0][0].has_o):
                twos += 1
            if (self._cells[1][2].has_o and not self._cells[2][2].has_x) or (not self._cells[1][2].has_x and self._cells[2][2].has_o):
                twos += 1
            if (self._cells[1][1].has_o and not self._cells[2][0].has_x) or (not self._cells[1][1].has_x and self._cells[2][0].has_o):
                twos += 1
        if i == 2 and j == 0:
            if (self._cells[2][1].has_o and not self._cells[2][2].has_x) or (not self._cells[2][1].has_x and self._cells[2][2].has_o):
                twos += 1
            if (self._cells[1][0].has_o and not self._cells[0][0].has_x) or (not self._cells[1][0].has_x and self._cells[0][0].has_o):
                twos += 1
            if (self._cells[1][1].has_o and not self._cells[0][2].has_x) or (not self._cells[1][1].has_x and self._cells[0][2].has_o):
                twos += 1
        return twos

    def lcheck_corner(self, i, j):
        twos = 0
        if i == 0 and j == 0:
            if (self._cells[0][1].has_x and not self._cells[0][2].has_o) or (not self._cells[0][1].has_o and self._cells[0][2].has_x):
                twos += 1
            if (self._cells[1][0].has_x and not self._cells[2][0].has_o) or (not self._cells[1][0].has_o and self._cells[2][0].has_x):
                twos += 1
            if (self._cells[1][1].has_x and not self._cells[2][2].has_o) or (not self._cells[1][1].has_o and self._cells[2][2].has_x):
                twos += 1
        if i == 2 and j == 2:
            if (self._cells[2][1].has_x and not self._cells[2][0].has_o) or (not self._cells[2][1].has_o and self._cells[2][0].has_x):
                twos += 1
            if (self._cells[1][2].has_x and not self._cells[0][2].has_o) or (not self._cells[1][2].has_o and self._cells[0][2].has_x):
                twos += 1
            if (self._cells[1][1].has_x and not self._cells[0][0].has_o) or (not self._cells[1][1].has_o and self._cells[0][0].has_x):
                twos += 1
        if i == 0 and j == 2:
            if (self._cells[0][1].has_x and not self._cells[0][0].has_o) or (not self._cells[0][1].has_o and self._cells[0][0].has_x):
                twos += 1
            if (self._cells[1][2].has_x and not self._cells[2][2].has_o) or (not self._cells[1][2].has_o and self._cells[2][2].has_x):
                twos += 1
            if (self._cells[1][1].has_x and not self._cells[2][0].has_o) or (not self._cells[1][1].has_o and self._cells[2][0].has_x):
                twos += 1
        if i == 2 and j == 0:
            if (self._cells[2][1].has_x and not self._cells[2][2].has_o) or (not self._cells[2][1].has_o and self._cells[2][2].has_x):
                twos += 1
            if (self._cells[1][0].has_x and not self._cells[0][0].has_o) or (not self._cells[1][0].has_o and self._cells[0][0].has_x):
                twos += 1
            if (self._cells[1][1].has_x and not self._cells[0][2].has_o) or (not self._cells[1][1].has_o and self._cells[0][2].has_x):
                twos += 1
        return twos

    def wcheck_center(self):
        twos = 0
        if (self._cells[0][2].has_o and not self._cells[2][0].has_x) or (self._cells[2][0].has_o and not self._cells[0][2].has_x):
            twos += 1
        if (self._cells[2][2].has_o and not self._cells[0][0].has_x) or (self._cells[0][0].has_o and not self._cells[2][2].has_x):
            twos += 1
        if (self._cells[0][1].has_o and not self._cells[2][1].has_x) or (self._cells[2][1].has_o and not self._cells[0][1].has_x):
            twos += 1
        if (self._cells[1][2].has_o and not self._cells[1][0].has_x) or (self._cells[1][0].has_o and not self._cells[1][2].has_x):
            twos += 1
        return twos

    def lcheck_center(self):
        twos = 0
        if (self._cells[0][2].has_x and not self._cells[2][0].has_o) or (self._cells[2][0].has_x and not self._cells[0][2].has_o):
            twos += 1
        if (self._cells[2][2].has_x and not self._cells[0][0].has_o) or (self._cells[0][0].has_x and not self._cells[2][2].has_o):
            twos += 1
        if (self._cells[0][1].has_x and not self._cells[2][1].has_o) or (self._cells[2][1].has_x and not self._cells[0][1].has_o):
            twos += 1
        if (self._cells[1][2].has_x and not self._cells[1][0].has_o) or (self._cells[1][0].has_x and not self._cells[1][2].has_o):
            twos += 1
        return twos

def tac(button_list, win):
    for button in button_list:
        button.destroy()
    necesary = tk.StringVar()
    necesary.set('Tic-Tac-Toe')
    title = tk.Label(win.get_root(), textvariable=necesary)
    title.place(x=1, y=1, width=win._width)
    necesary2 = tk.StringVar()
    necesary2.set("The Rules:\nthe original. If you don't already know how to play this game, you'll pick it up quickly")
    rules = tk.Label(win.get_root(), textvariable=necesary2, wraplength=190, bg="#00C000", bd=3, relief="raised")
    rules.place(x=10, y=150, width=200, height=300)
    button1 = tk.Button(win.get_root(), bg="#00C000", activebackground="#009000", text="Local Multiplayer",
                        anchor="center")
    button2 = tk.Button(win.get_root(), bg="#00C000", activebackground="#009000", text="Singleplayer",
                        anchor="center")
    button1['command'] = lambda button1=button1, button2=button2, rules=rules, win=win: make_rboard(button1, button2, rules, win)
    button2['command'] = lambda button1=button1, button2=button2, rules=rules, win=win: make_AI_rboard(button1, button2, rules, win)
    button1.place(x=win._width/3, y=win._height/5, width=win._width/3, height=win._height/5)
    button2.place(x=win._width/3, y=(win._height/5)*3, width=win._width/3, height=win._height/5)
    win.wait_for_close()

def inv(button_list, win):
    for button in button_list:
        button.destroy()
    necesary = tk.StringVar()
    necesary.set('Inverse Tic-Tac-Toe')
    title = tk.Label(win.get_root(), textvariable=necesary)
    title.place(x=1, y=1, width=win._width)
    necesary2 = tk.StringVar()
    necesary2.set("The Rules:\nthe original, but the goal is to make your opponent get three in a row")
    rules = tk.Label(win.get_root(), textvariable=necesary2, wraplength=190, bg="#00C000", bd=3, relief="raised")
    rules.place(x=10, y=150, width=200, height=300)
    button1 = tk.Button(win.get_root(), bg="#00C000", activebackground="#009000", text="Local Multiplayer",
                        anchor="center")
    button2 = tk.Button(win.get_root(), bg="#00C000", activebackground="#009000", text="Singleplayer",
                        anchor="center")
    button1['command'] = lambda button1=button1, button2=button2, rules=rules, win=win: make_iboard(button1, button2, rules, win)
    button2['command'] = lambda button1=button1, button2=button2, rules=rules, win=win: make_AI_iboard(button1, button2, rules, win)
    button1.place(x=win._width/3, y=win._height/5, width=win._width/3, height=win._height/5)
    button2.place(x=win._width/3, y=(win._height/5)*3, width=win._width/3, height=win._height/5)
    win.wait_for_close()

def oat(button_list, win):
    for button in button_list:
        button.destroy()
    necesary = tk.StringVar()
    necesary.set('Tick-oaT-Two')
    title = tk.Label(win.get_root(), textvariable=necesary)
    title.place(x=1, y=1, width=win._width)
    necesary2 = tk.StringVar()
    necesary2.set('The Rules:\nlike regular tic-tac-toe, but with a twist. one player plays vertical lines, while the other plays horizontal lines. When two players play on the same space, a cross is formed. The player to finish a row of three crosses first is the winner. You can not play a line on the same square your opponent played on in their previous turn, as this makes player 2 unable to lose. Have fun!')
    rules = tk.Label(win.get_root(), textvariable=necesary2, wraplength=190, bg="#00C000", bd=3, relief="raised")
    rules.place(x=10, y=150, width=200, height=300)
    button1 = tk.Button(win.get_root(), bg="#00C000", activebackground="#009000", text="Local Multiplayer",
                        anchor="center")
    button2 = tk.Button(win.get_root(), bg="#00C000", activebackground="#009000", text="Singleplayer",
                        anchor="center")
    button1['command'] = lambda button1=button1, button2=button2, rules=rules, win=win: make_board(button1, button2, rules, win)
    button2['command'] = lambda button1=button1, button2=button2, rules=rules, win=win: make_AI_board(button1, button2, rules, win)
    button1.place(x=win._width/3, y=win._height/5, width=win._width/3, height=win._height/5)
    button2.place(x=win._width/3, y=(win._height/5)*3, width=win._width/3, height=win._height/5)
    win.wait_for_close()

def make_board(button1, button2, rules, win):
    button1.destroy()
    button2.destroy()
    rules.destroy()
    b1 = Board(100, 100, 150, win)

def make_rboard(button1, button2, rules, win):
    button1.destroy()
    button2.destroy()
    rules.destroy()
    b1 = RBoard(100, 100, 150, win)

def make_iboard(button1, button2, rules, win):
    button1.destroy()
    button2.destroy()
    rules.destroy()
    b1 = IBoard(100, 100, 150, win)

def make_AI_board(button1, button2, rules, win):
    button1.destroy()
    button2.destroy()
    rules.destroy()
    b1 = AI_Board(100, 100, 150, win)

def make_AI_rboard(button1, button2, rules, win):
    button1.destroy()
    button2.destroy()
    rules.destroy()
    b1 = AI_RBoard(100, 100, 150, win)

def make_AI_iboard(button1, button2, rules, win):
    button1.destroy()
    button2.destroy()
    rules.destroy()
    b1 = AI_IBoard(100, 100, 150, win)
