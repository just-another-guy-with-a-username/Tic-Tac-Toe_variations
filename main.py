from graphics import Window
from board import Board

def main():
    win = Window(800, 600)
    b1 = Board(100, 250, 150, win)
    win.wait_for_close()

main()
