import PySide6 as QT
from PySide6.QtWidgets import QApplication
import os
import sys
import time
import random
import threading
from shellmagotchi import Shellmagotchi as SM
from game_window import ShellmagotchiGame

gotchi = SM("Tester")

def handle_decay():
    while True:
        gotchi.update_needs()
        time.sleep(1)

decay_thread = threading.Thread(target=handle_decay)
decay_thread.daemon = True
decay_thread.start()

def main(): 
    while True:
        gotchi.update_needs()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = ShellmagotchiGame()
    game.show()
    sys.exit(app.exec())