import PySide6 as QT
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
import os
import sys
import time
import random
import threading
from shellmagotchi import Shellmagotchi as SM
from game_window import ShellmagotchiGame

# Low priority
# TODO: Flavor text, flavor text everywhere
# TODO: Debugging, optimizing, cleaning up code
# TODO: Fix broken animation for "move"

def main_loop(game):
    if game.gotchi and game.gotchi.alive:
        game.gotchi.update_needs()
        happiness_decay_rate = game.gotchi.happiness_decay()
        game.gotchi.update_happiness(happiness_decay_rate)
        game.gotchi.check_runaway()
        game.gotchi.check_death()
        game.gotchi.update_life_stage()
        game.update_ui(update_character_image=False) # Animations are run seperate to avoid overwrite
        print("Main looped")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = ShellmagotchiGame(debug=True)

    timer = QTimer()
    timer.timeout.connect(lambda: main_loop(game))
    timer.start(1000)

    game.show()
    sys.exit(app.exec())