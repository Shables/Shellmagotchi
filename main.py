import PySide6 as QT
from PySide6.QtWidgets import QApplication
import os
import sys
import time
import random
import threading
from shellmagotchi import Shellmagotchi as SM
from game_window import ShellmagotchiGame


# Ugh still trying to get the formatting in QT correct -- Got the multithreading working though so the needs continously update and the user can put in an input at any time.

# TODO: Implement happiness feature and if happiness drops too low then gotchi runs away.. 
# every 1min it will randomly decide to come back, also its needs will replenish at a rate of 1% per 1min 
# and the chance is based on how high needs are. 

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