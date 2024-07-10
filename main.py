from graphics import Window
from board import Board, AI_Board, RBoard, AI_RBoard, IBoard, AI_IBoard, QBoard, tac, oat, inv, qua, make_rboard, make_board, make_iboard, make_qboard, make_AI_rboard, make_AI_board, make_AI_iboard
from cell import QCell
import tkinter as tk
import time


def main():
    window_length = 800
    window_height = 600
    win = Window(window_length, window_height, "Tic-Tac-Toe")
    necesary = tk.StringVar()
    necesary.set('Game Select')
    title = tk.Label(win.get_root(), textvariable=necesary)
    title.place(x=1, y=1, width=win._width)
    button1 = tk.Button(win.get_root(), bg="#00C000", activebackground="#009000", text="Tic-Tac-Toe",
                        anchor="center")
    button2 = tk.Button(win.get_root(), bg="#00C000", activebackground="#009000", text="Tick-oaT-Two",
                        anchor="center")
    button3 = tk.Button(win.get_root(), bg="#00C000", activebackground="#009000", text="Inverse Tic-Tac-Toe",
                        anchor="center")
    button4 = tk.Button(win.get_root(), bg="#00C000", activebackground="#009000", text="Quantum Tic-Tac-Toe",
                        anchor="center")
    button1['command'] = lambda button1=button1, button2=button2, button3=button3, win=win: tac([button1, button2, button3, button4], win)
    button2['command'] = lambda button1=button1, button2=button2, button3=button3, win=win: oat([button1, button2, button3, button4], win)
    button3['command'] = lambda button1=button1, button2=button2, button3=button3, win=win: inv([button1, button2, button3, button4], win)
    button4['command'] = lambda button1=button1, button2=button2, button3=button3, win=win: qua([button1, button2, button3, button4], win)
    button1.place(x=window_length/9, y=window_height/5, width=window_length/3, height=window_height/5)
    button2.place(x=window_length/9, y=(window_height/5)*3, width=window_length/3, height=window_height/5)
    button3.place(x=5*(window_length/9), y=(window_height/5), width=window_length/3, height=window_height/5)
    button4.place(x=5*(window_length/9), y=(window_height/5)*3, width=window_length/3, height=window_height/5)
    win.wait_for_close()

main()
