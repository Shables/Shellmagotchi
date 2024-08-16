import os
import sys
import time
import random



class Shellmagotchi:
    def __init__(self, name):
        self.name = name
        self._hunger = 100
        self._thirst = 100
        self._sleep = 100
        self._hygiene = 100
        self._bladder = 100
        self._socialize = 100
        self.life_stage = 'Egg'
        self.last_update_time = time.time()

# Private values for ensuring needs stay equal to and between 0 and 100
    @property
    def hunger(self):
        return self._hunger
    
    @hunger.setter
    def hunger(self, value):
        self._hunger = max(0, min(100, value))

    @property
    def thirst(self):
        return self._thirst
    
    @thirst.setter
    def thirst(self, value):
        self._thirst = max(0, min(100, value))

    @property
    def sleep(self):
        return self._sleep
    
    @sleep.setter
    def sleep(self, value):
        self._sleep = max(0, min(100, value))

    @property
    def hygiene(self):
        return self._hygiene
    
    @hygiene.setter
    def hygiene(self, value):
        self._hygiene = max(0, min(100, value))

    @property
    def bladder(self):
        return self._bladder
    
    @bladder.setter
    def bladder(self, value):
        self._bladder = max(0, min(100, value))

    @property
    def socialize(self):
        return self._socialize
    
    @socialize.setter
    def socialize(self, value):
        self._socialize = max(0, min(100, value))

# Functions for satiating the needs for gotchi 
    def feed(self):
        self.hunger += 20
        print("Gotchi fed")

    def give_water(self):
        self.thirst += 20
        print("Gotchi thirsted")

    def tuck_in(self):
        self.sleep += 20
        print("Gotchi slept")

    def bathe(self):
        self.hygiene += 20
        print("Gotchi bathed")

    def potty(self):
        self.bladder += 20
        print("Gotchi pottied")

    def socialize(self):
        self.socialize += 20
        print("Gotchi socialized")

# Continously update and track the changing needs  
    def update_needs(self, hunger, thirst, sleep, hygiene, bladder, socialize):
        current_time = time.time()
        elapsed_time = current_time - self.last_update_time
        self.needs_decay(elapsed_time)
        self.save_last_update_time()
        print(f"Current Needs -- Hunger: {hunger}, Thirst: {thirst}, Sleep: {sleep}, Hygiene: {hygiene}, Bladder: {bladder}, Socialize: {socialize}")

    def needs_decay(self, elapsed_time):
        decay_rate = 1 # points per second
        decay_amount = decay_rate * elapsed_time
        self.hunger = max(0, self._hunger - decay_amount)

# Save/Load current time to seperate file to track needs decay
    def save_last_update_time(self):
        self.last_update_time = time.time()
        try:
            with open ('last_update_time.txt', 'w') as file:
                file.write(str(self.last_update_time))
        except FileNotFoundError:
            print("There was an error in saving the time to .txt file")

    def load_last_update_time(self):
        try:
            with open('last_update_time.txt', 'r') as file:
                self.last_update_time = float(file.read())
        except FileNotFoundError:
            with open('last_update_time.txt', 'w') as file:
                self.last_update_time = time.time()
                file.write(str(self.last_update_time))

