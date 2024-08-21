import os
import sys
import time
import random
import threading
from PySide6.QtCore import Signal, QObject
from datetime import datetime
from colorama import Fore, Back, Style


class Shellmagotchi(QObject):
    rebirthRequested = Signal()

    def __init__(self, name):
        super().__init__() # Superclass initializer MUST be called
        self.name = name
        self._hunger = 100
        self._thirst = 100
        self._sleep = 100
        self._hygiene = 100
        self._bladder = 100
        self._socialize = 100
        self.life_stage = 'Egg'
        self.last_update_time = time.time()
        self.birth_time = datetime.now()
        self._happiness = 100
        self.age = 0
        self.alive = True
        self.dying = False
        self.runaway = False
        self.rebirthing = False

    @staticmethod
    def clamp(value, minimum=0, maximum=100):
        return max(minimum, min(maximum, value))

# Private values for ensuring needs stay equal to and between 0 and 100
    @property
    def hunger(self):
        return self._hunger
    
    @hunger.setter
    def hunger(self, value):
        self._hunger = self.clamp(value)

    @property
    def thirst(self):
        return self._thirst
    
    @thirst.setter
    def thirst(self, value):
        self._thirst = self.clamp(value)

    @property
    def sleep(self):
        return self._sleep
    
    @sleep.setter
    def sleep(self, value):
        self._sleep = self.clamp(value)

    @property
    def hygiene(self):
        return self._hygiene
    
    @hygiene.setter
    def hygiene(self, value):
        self._hygiene = self.clamp(value)

    @property
    def bladder(self):
        return self._bladder
    
    @bladder.setter
    def bladder(self, value):
        self._bladder = self.clamp(value)

    @property
    def socialize(self):
        return self._socialize
    
    @socialize.setter
    def socialize(self, value):
        self._socialize = self.clamp(value)

    @property
    def happiness(self):
        return self._happiness
    
    @happiness.setter
    def happiness(self, value):
        self._happiness = self.clamp(value)

# Functions for satiating the needs for gotchi 
    def feed(self):
        self.hunger += 100
        print("Gotchi fed")

    def give_water(self):
        self.thirst += 100
        print("Gotchi thirsted")

    def tuck_in(self):
        self.sleep += 100
        print("Gotchi slept")

    def bathe(self):
        self.hygiene += 100
        print("Gotchi bathed")

    def potty(self):
        self.bladder += 100
        print("Gotchi pottied")

    def social(self):
        self.socialize += 100
        print("Gotchi socialized")

# Continously update and track the changing needs  
    def update_needs(self):
        if not self.alive:
            self.hunger == 0
            self.thirst == 0
            self.sleep == 0
            self.hygiene == 0
            self.bladder == 0
            self.socialize == 0
        elif self.alive:
            current_time = time.time()
            elapsed_time = current_time - self.last_update_time
            self.needs_decay(elapsed_time)
            self.save_last_update_time()
            print(f"Current Needs -- Hunger: {self.hunger:.2f}, Thirst: {self.thirst:.2f}, Sleep: {self.sleep:.2f}, Hygiene: {self.hygiene:.2f}, Bladder: {self.bladder:.2f}, Socialize: {self.socialize:.2f}")
            print(f"# Debug: Alive - {self.alive}, Runaway - {self.runaway}, Dying - {self.dying}, Rebirthing - {self.rebirthing}")

    def needs_decay(self, elapsed_time):
        decay_rate = 1 # points per second
        decay_amount = decay_rate * elapsed_time
        self.hunger = max(0, self.hunger - decay_amount)
        self.thirst = max(0, self.thirst - (decay_amount * 3)) # Faster for death debugging
        self.sleep = max(0, self.sleep - decay_amount)
        self.hygiene = max(0, self.hygiene - decay_amount)
        self.bladder = max(0, self.bladder - decay_amount)
        self.socialize = max(0, self.socialize - decay_amount)

# Reduce Happiness Faster Based on Need Breakpoints
# 75% < x = No lost happiness/Happy
# 50% - 74 <= Slow Loss
# 25% - 49% <= Fast Loss
# 0% - 24% <= Near-instant loss
    def happiness_decay(self):
        if not self.alive:
            self.happiness == 0 # It's dead
        elif self.alive:
            current_needs = sum([self.hunger, self.thirst, self.sleep, self.hygiene, self.bladder, self.socialize]) # Total Maxed Needs
            percent_needs_met = (current_needs / 600) * 100
            print(Fore.RED + f"Current Percentage of Needs Met: {percent_needs_met:.2f}" + Style.RESET_ALL)

            if percent_needs_met >= 75.0:
                happiness_decay_rate = 1.0
                self.happiness += 1
            elif percent_needs_met >= 50.0:
                happiness_decay_rate = 0.95
            elif percent_needs_met >= 25:
                happiness_decay_rate = 0.90
            elif percent_needs_met >= 0:
                happiness_decay_rate = 0.80
            else:
                print("Error with Happiness Decay method")
            return happiness_decay_rate

    def update_happiness(self, happiness_decay_rate):
        self.happiness = self.happiness * happiness_decay_rate
        print(Fore.YELLOW + f"Current Happiness: {self.happiness:.2f}" + Style.RESET_ALL)
        
# Check for Runaway
    def check_runaway(self):
        if not self.runaway and not self.dying:
            if self.happiness < 20:
                runaway_probability = max(0, min(1, (20 - self.happiness) / 20)) # Probably broken
                if random.random() < runaway_probability:
                    self.runaway = True
                    print(f"{self.name} has run away!")
            elif self.runaway:
                if random.random() < 0.01 * (self.happiness / 100): # Return chance based on happiness
                    self.runaway = False
                    self.replenish_needs()
                    print(f"{self.name} has returned!")
                else:
                    self.happiness += 1

# Replenish All Needs
    def replenish_needs(self):
        for need in ['hunger', 'thirst', 'sleep', 'hygiene', 'bladder', 'socialize']:
            setattr(self, need, min(getattr(self, need) + 1, 100))

# Check for death
    def check_death(self):
        if self.alive and not self.dying:
            if self.hunger <= 0 or self.thirst <= 0:
                self.dying = True
                print("WARNING: GOTCHI DYING OF THIRST AND HUNGER")
                self.death_timer = threading.Timer(5, self.confirm_dead)
                self.death_timer.start()

    def confirm_dead(self):
        if self.alive and self.dying:
            if self.hunger <= 0 or self.thirst <= 0:
                print(f"{self.name} has died!")
                self.alive = False
                print("A moment of silence...")
                time.sleep(5)
                self.rebirth()
            else:
                self.dying = False
                print(f"{self.name} has started to recover from malnutrition")

# Rebirth the gotchi after some time
    def rebirth(self):
        if self.alive == False and self.rebirthing == False:
            self.rebirthing = True
            print("rebirth() has changed self.rebirthing to True")
            self.rebirthRequested.emit()
            print("Sending signal for rebirth")

# Save the dead gotchi to a txt file for archive
    def archive_gotchi(self):
        data_to_archive = {
            "name": self.name,
            "age": self.age,
            "life_stage": self.life_stage,
            "death_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            with open("gotchi_graveyard.txt", "a") as f: # a does append, just learned that
                f.write(str(data_to_archive) + "\n") # Newline after each one
            print(f"{self.name}'s memory has been preserved in the gotchi_graveyard")
        except IOError:
            print("Error: Could not archive gotchi data")


# Life Stages
    def update_life_stage(self):
        age_seconds = 1 # Debug
        age_minutes = 60 # Debug
        age_days = 86400
        current_time = datetime.now()
        self.age = (current_time - self.birth_time).total_seconds() / age_seconds # Age in minutes
        # Check if dead first, then runaway, then lifestage
        if self.alive == False:
            self.life_stage = 'Dead'
        elif self.runaway == True:
            self.life_stage = 'Runaway'
        else:    
            if self.age < 1:
                self.life_stage = 'Egg'
            elif self.age < 7:
                self.life_stage = 'Child'
            elif self.age < 14:
                self.life_stage = 'Teen'
            elif self.age < 21:
                self.life_stage = 'Adult'
            elif self.age < 30:
                self.life_stage = 'Mature'
            else:
                self.life_stage = 'Elder'

# Save/Load current time to seperate file to track needs decay while user away
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

