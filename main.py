import PySide6 as QT
import os
import sys
import time
import random
import threading
from shellmagotchi import Shellmagotchi as SM

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
        user_input = str(input("Type any command: \n"))

        if user_input == 'feed':
            gotchi.hunger()
        elif user_input == 'water':
            gotchi.thirst()
        elif user_input == 'bathe':
            gotchi.hygiene()
        elif user_input == 'tuck-in':
            gotchi.tuck_in()
        elif user_input == 'potty':
            gotchi.bladder()
        elif user_input == 'socialize':
            gotchi.socialize()


if __name__ == '__main__':
    main()