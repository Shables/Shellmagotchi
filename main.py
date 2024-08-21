import PySide6 as QT
from PySide6.QtWidgets import QApplication
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
    while True:
        if gotchi is not None:
            gotchi.update_needs()
            happiness_decay_rate = gotchi.happiness_decay()
            gotchi.update_happiness(happiness_decay_rate)
            gotchi.check_runaway()
            gotchi.check_death()
            gotchi.update_life_stage()
            game.update_ui()
        time.sleep(2.5)
        print("Main Looped")

def start_main_loop(gotchi, game):
    main_thread = threading.Thread(target=main_loop, args=(gotchi, game))
    main_thread.daemon = True
    main_thread.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = ShellmagotchiGame()

    # Connecting a signal from game_window to main.py to trigger main loop
    game.gotchiCreated.connect(lambda gotchi: start_main_loop(gotchi, game))

    game.show()
    sys.exit(app.exec())



