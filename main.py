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
# TODO: Balance the needs decay values
# TODO: Flavor text, flavor text everywhere
# TODO: Lifestages affect needs decay as well as flavor text - simple
# TODO: Implement cute movement animations to try and give the gotchi some life
# TODO: Minigames like guess the number, guess the word, simple math problems, hide and seek, etc. Increases socialize stat

# Medium priority
# TODO: Debugging, optimizing, cleaning up code
# TODO: Fix time save time load feature so it accurately updates values and uses save states
# TODO: Create save states for the Tomagatchi itself so player can have perpetual progress

def main_loop(gotchi, game):
    if gotchi and gotchi.alive:
        gotchi.update_needs()
        happiness_decay_rate = gotchi.happiness_decay()
        gotchi.update_happiness(happiness_decay_rate)
        gotchi.check_runaway()
        gotchi.check_death()
        gotchi.update_life_stage()
        game.update_ui()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = ShellmagotchiGame(debug=True)

    timer = QTimer()
    timer.timeout.connect(lambda: main_loop(game.gotchi, game))
    timer.start(2000)

    game.show()
    sys.exit(app.exec())