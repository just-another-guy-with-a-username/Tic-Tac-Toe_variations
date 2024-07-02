from graphics import Window
from board import Board, AI_Board, RBoard, AI_RBoard
import tkinter as tk


def main():
    window_length = 800
    window_height = 600
    win = Window(window_length, window_height)
    necesary = tk.StringVar()
    necesary.set('Game Select')
    title = tk.Label(win.get_root(), textvariable=necesary)
    title.place(x=1, y=1, width=win._width)
    button1 = tk.Button(win.get_root(), bg="#00C000", activebackground="#009000", text="Tic-Tac-Toe",
                        anchor="center")
    button2 = tk.Button(win.get_root(), bg="#00C000", activebackground="#009000", text="Tick-oaT-Two",
                        anchor="center")
    button1['command'] = lambda button1=button1, button2=button2, win=win: tac([button1, button2], win)
    button2['command'] = lambda button1=button1, button2=button2, win=win: oat([button1, button2], win)
    button1.place(x=window_length/3, y=window_height/5, width=window_length/3, height=window_height/5)
    button2.place(x=window_length/3, y=(window_height/5)*3, width=window_length/3, height=window_height/5)
    win.wait_for_close()

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

def make_rboard(button1, button2, rules, win):
    button1.destroy()
    button2.destroy()
    rules.destroy()
    b1 = RBoard(100, 100, 150, win)

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

def make_AI_rboard(button1, button2, rules, win):
    button1.destroy()
    button2.destroy()
    rules.destroy()
    b1 = AI_RBoard(100, 100, 150, win)

main()
