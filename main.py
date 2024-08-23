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
# TODO: Egg hatching animation
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

        # Flavor text messages for info_frame
        if random.randint(1, 10) == 1:
            game.gotchi.display_life_stage_flavor_text()
        game.gotchi.display_need_based_messages()

        game.update_ui(update_character_image=False)
        print("Main looped")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = ShellmagotchiGame(debug=True)

    timer = QTimer()
    timer.timeout.connect(lambda: main_loop(game))
    timer.start(1000)

    game.show()
    sys.exit(app.exec())