from graphics import Window
from board import Board, AI_Board
import tkinter as tk


def main():
    window_length = 800
    window_height = 600
    win = Window(window_length, window_height)
    necesary = tk.StringVar()
    necesary.set('Tick-oaT-Two')
    title = tk.Label(win.get_root(), textvariable=necesary)
    title.place(x=1, y=1, width=window_length)
    button1 = tk.Button(win.get_root(), bg="#00C000", activebackground="#009000", text="Local Multiplayer",
                        anchor="center")
    button2 = tk.Button(win.get_root(), bg="#00C000", activebackground="#009000", text="Singleplayer",
                        anchor="center")
    button1['command'] = lambda button1=button1, button2=button2, win=win: make_board(button1, button2, win)
    button2['command'] = lambda button1=button1, button2=button2, win=win: make_AI_board(button1, button2, win)
    button1.place(x=window_length/3, y=window_height/5, width=window_length/3, height=window_height/5)
    button2.place(x=window_length/3, y=(window_height/5)*3, width=window_length/3, height=window_height/5)
    win.wait_for_close()

def make_board(button1, button2, win):
    button1.destroy()
    button2.destroy()
    b1 = Board(100, 100, 150, win)

def make_AI_board(button1, button2, win):
    button1.destroy()
    button2.destroy()
    b1 = AI_Board(100, 100, 150, win)

main()
