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
    button1.place(x=window_length/3, y=window_height/5, width=window_length/3, height=window_height/5)
    button2.place(x=window_length/3, y=(window_height/5)*3, width=window_length/3, height=window_height/5)
    win.wait_for_close()

def make_board(button1, button2, rules, win):
    button1.destroy()
    button2.destroy()
    rules.destroy()
    b1 = Board(100, 100, 150, win)

def make_AI_board(button1, button2, rules, win):
    button1.destroy()
    button2.destroy()
    rules.destroy()
    b1 = AI_Board(100, 100, 150, win)

main()
