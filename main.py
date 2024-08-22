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
# TODO: MAYBE: Minigames like guess the number, guess the word, simple math problems, hide and seek, etc. Increases socialize stat
# TODO: Debugging, optimizing, cleaning up code

## Medium priority
# TODO: Implement cute movement animations to try and give the gotchi some life

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