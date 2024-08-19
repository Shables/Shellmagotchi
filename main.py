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
# and the chance is based on how high needs are. -- Runaway should be a product of current needs vs max needs

# TODO: Balance the needs decay values, implement the death if Hunger or Thirst == 0  

# TODO: Minigames like guess the number, guess the word, simple math problems, hide and seek, etc. Increases socialize stat

# TODO: Different lifestages: Child, Teen, Adult, Mature, Elder, [dead]. Lifestages affect needs decay as well as flavor text - simple

# TODO: Implement cute movement animations to try and give the gotchi some life

# TODO: Implement death and rebirth feature -- SHOULD INDIVIDUAL PERSONALITY STATS BE A THING????


def main_loop(gotchi, game):
    while True:
        gotchi.update_needs()
        happiness_decay_rate = gotchi.happiness_decay()
        gotchi.update_happiness(happiness_decay_rate)
        print(f"Main happiness: {gotchi.happiness}")
        gotchi.check_runaway()
        gotchi.check_death()
        gotchi.update_life_stage()
        game.update_ui()
        time.sleep(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gotchi = SM("Tester")
    game = ShellmagotchiGame(gotchi)

    main_thread = threading.Thread(target=main_loop, args=(gotchi, game))
    main_thread.daemon = True
    main_thread.start()

    game.show()
    sys.exit(app.exec())