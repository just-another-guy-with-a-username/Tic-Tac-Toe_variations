from graphics import Window
from board import Board, AI_Board
import tkinter as tk


def main():
    win = Window(800, 600)
    b1 = AI_Board(100, 100, 150, win)
    win.wait_for_close()

main()
