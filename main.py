from graphics import Window
from board import Board, AI_Board, RBoard, AI_RBoard, IBoard, AI_IBoard, QBoard
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

def qua(button_list, win):
    for button in button_list:
        button.destroy()
    necesary = tk.StringVar()
    necesary.set('Quantum Tic-Tac-Toe')
    title = tk.Label(win.get_root(), textvariable=necesary)
    title.place(x=1, y=1, width=win._width)
    necesary2 = tk.StringVar()
    necesary2.set("The Rules:\nquantum tic-tac-toe is the most challenging version to learn, but the most rewarding to master. There are three main concepts introduced in this version of tic-tac-toe that make it so different. The first new concept is quantum superposition. Every turn, a player plays an x or o that is in a super position of being in two squares. For example, on turn 1, player x might put an x in a superposition of being in square one and three. On the next turn, o may place an o in a superposition of being in both square one and square nine. The o and the x that are both superimposed in square one are now entangled. on the next turn, player x could choose to play an x that is superimposed in both square three and square nine. At this point, squares three, nine, and one are connected in a loop. This loop is formed because move o2 (which is how these moves are marked in the game) connects square one to square nine. Square nine is connected by move x3 to square three, which in turn connects back to square one by move x1. Whenever a loop like this is created, it causes the superimposed moves to collapse into their final states, similarly to how particles in a state of quantum superposition collapse when they are observed. The player who did not create the loop determines which deirection the loop will collapse in. In this example, o gets to pick. O can either force move o2 to collapse into cell nine, forcing move x3 into square three, which in turn forces move x1 into square one. Squares containing final states may not be entangled with other squares, and are the ones used to calculate three in a rows. In the case that a collapse leads to each player having one three in a row, the player who's three in a row has a lower highest move number wins. For example, an x three in a row containing moves x1, x3, and x7 would lose to an o three in a row containing moves o2, o4, and o6.")
    rules = tk.Label(win.get_root(), textvariable=necesary2, wraplength=win._width-20, bg="#00C000", bd=3, relief="raised")
    rules.place(x=0, y=(win._height/7)*3, width=win._width, height=(win._height/7)*4)
    button1 = tk.Button(win.get_root(), bg="#00C000", activebackground="#009000", text="Local Multiplayer",
                        anchor="center")
    button1['command'] = lambda button1=button1, rules=rules, win=win: make_qboard(button1, rules, win)
    button1.place(x=win._width/3, y=win._height/5, width=win._width/3, height=win._height/5)
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

def make_qboard(button1, rules, win):
    button1.destroy()
    rules.destroy()
    b1 = QBoard(100, 100, 150, win)

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

main()
