from graphics import Window
from board import Board
import tkinter as tk


def main():
    win = Window(800, 600)
    b1 = Board(100, 100, 150, win)
    win.wait_for_close()

main()
