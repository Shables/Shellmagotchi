import os
import sys
import time
import random
import threading
from PySide6.QtCore import Signal, QObject
from datetime import datetime, timedelta
from save_system import save_game, load_game, delete_save
from colorama import Fore, Back, Style
from enum import Enum

class LifeStage(Enum):
    EGG = "Egg"
    CHILD = "Child"
    TEEN = "Teen"
    ADULT = "Adult"
    MATURE = "Mature"
    ELDER = "Elder"
    DEAD = "Dead"
    RUNAWAY = "Runaway"

need_weights = {
    LifeStage.EGG: {
        "hunger": 0.1,
        "thirst": 0.1,
        "sleep": 0.1,
        "hygiene": 0.1,
        "bladder": 0.1,
        "socialize": 0.1
    },
    LifeStage.CHILD: {
        "hunger": 1.0,
        "thirst": 1.0,
        "sleep": 1.2,
        "hygiene": 0.8,
        "bladder": 1.2,
        "socialize": 1.0
    },
    LifeStage.TEEN: {
        "hunger": 1.2,
        "thirst": 1.0,
        "sleep": 1.0,
        "hygiene": 0.8,
        "bladder": 1.0,
        "socialize": 1.2
    },
    LifeStage.ADULT: {
        "hunger": 1.0,
        "thirst": 1.2,
        "sleep": 1.0,
        "hygiene": 1.2,
        "bladder": 1.0,
        "socialize": 0.8
    },
    LifeStage.MATURE: {
        "hunger": 0.8,
        "thirst": 1.2,
        "sleep": 1.2,
        "hygiene": 1.0,
        "bladder": 1.2,
        "socialize": 1.0
    },
    LifeStage.ELDER: {
        "hunger": 0.6,
        "thirst": 0.8,
        "sleep": 1.5,
        "hygiene": 0.8,
        "bladder": 1.5,
        "socialize": 1.5
    }
}

class Shellmagotchi(QObject):
    rebirthRequested = Signal()
    died = Signal()

    def __init__(self, name):
        super().__init__() # Superclass initializer MUST be called
        save_data, last_update_time = load_game()

        if save_data:
            self.load_from_save(save_data)
        else:
            self.initialize_new(name)

        self.last_update_time = last_update_time or time.time()

        # Check if gotchi died while game closed
        if self.alive:
            elapsed_time = time.time() - self.last_update_time
            self.needs_decay(elapsed_time * 0.01) # 1% of needs decay while offline
            self.check_death()
        if not self.alive:
            self.zero_stats()
            self.archive_gotchi

    def initialize_new(self, name):
        self.name = name
        self._hunger = 100
        self._thirst = 100
        self._sleep = 100
        self._hygiene = 100
        self._bladder = 100
        self._socialize = 100
        self.life_stage = LifeStage.EGG
        self.last_update_time = time.time()
        self.birth_time = datetime.now()
        self._happiness = 100
        self.age = 0
        self.alive = True
        self.runaway = False
        self.dying = False
        self.rebirthing = False
        self.rebirth_signal_sent = False
        self.flavor_text = ''
        self.need_message = ''
        self.last_flavor_text = ''
        self.last_need_message = ''


    def load_from_save(self, save_data):
        self.name = save_data["name"]
        self.birth_time = datetime.fromisoformat(save_data["birth_time"])
        self._hunger = save_data["hunger"]
        self._thirst = save_data["thirst"]
        self._sleep = save_data["sleep"]
        self._hygiene = save_data["hygiene"]
        self._bladder = save_data["bladder"]
        self._socialize = save_data["socialize"]
        self._happiness = save_data["happiness"]
        self.life_stage = LifeStage(save_data["life_stage"])
        self.alive = save_data["alive"]
        self.runaway = save_data["runaway"]
        self.dying = save_data["dying"]
        self.rebirthing = save_data["rebirthing"]
        self.rebirth_signal_sent = save_data["rebirth_signal_sent"]

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
            current_time = time.time()
            elapsed_time = current_time - self.last_update_time
            self.needs_decay(elapsed_time)
            self.last_update_time = current_time
            save_game(self, self.last_update_time)

    def needs_decay(self, elapsed_time):
        decay_rate = 1 # points per second
        decay_amount = decay_rate * elapsed_time

        weights = need_weights.get(self.life_stage, {})

        # Needs decay based on weights based on LifeStage
        self.hunger = max(0, self.hunger - (decay_amount * 0.01 * weights.get("hunger", 1.0)))
        self.thirst = max(0, self.thirst - (decay_amount * 0.02 * weights.get("thirst", 1.0)))
        self.sleep = max(0, self.sleep - (decay_amount * 0.035 * weights.get("sleep", 1.0)))
        self.hygiene = max(0, self.hygiene - (decay_amount * 0.015 * weights.get("hygiene", 1.0)))
        self.bladder = max(0, self.bladder - (decay_amount * 0.04 * weights.get("bladder", 1.0)))
        self.socialize = max(0, self.socialize - (decay_amount * 0.025 * weights.get("socialize", 1.0)))

# Reduce Happiness Faster Based on % of needs met Breakpoints
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
        if not self.alive:
            print("Can't calculate happiness on dead gotchi")
        else:
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

# Zero out stats (for death)
    def zero_stats(self):
        if not self.alive:
            self.hunger == 0
            self.thirst == 0
            self.sleep == 0
            self.hygiene == 0
            self.bladder == 0
            self.socialize == 0
            self.happiness == 0

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
                self.life_stage = LifeStage.DEAD
                self.archive_gotchi()
                self.zero_stats()
                self.died.emit()
                print("A moment of silence...")
                self.rebirth()
            else:
                self.dying = False
                print(f"{self.name} has started to recover from malnutrition")

# Rebirth the gotchi after some time
    def rebirth(self):
        if not self.alive and not self.rebirthing and not self.rebirth_signal_sent:
            self.rebirthing = True
            print("rebirth() has changed self.rebirthing to True")
            self.rebirthRequested.emit()
            print("Sending signal for rebirth")
            self.rebirth_signal_sent = True

# Save the dead gotchi to a txt file for archive
    def archive_gotchi(self):
        data_to_archive = {
            "name": self.name,
            "age": self.age,
            "life_stage": self.life_stage.value,
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
        self.age = (current_time - self.birth_time).total_seconds() / age_minutes # Age in minutes
        # Check if dead first, then runaway, then lifestage
        if self.alive == False:
            self.life_stage = LifeStage.DEAD
        elif self.runaway == True:
            self.life_stage = LifeStage.RUNAWAY
        else:    
            if self.age < 1:
                self.life_stage = LifeStage.EGG
            elif self.age < 30:
                self.life_stage = LifeStage.CHILD
            elif self.age < 90:
                self.life_stage = LifeStage.TEEN
            elif self.age < 180:
                self.life_stage = LifeStage.ADULT
            elif self.age < 360:
                self.life_stage = LifeStage.MATURE
            else:
                self.life_stage = LifeStage.ELDER

# Flavor text based on lifestage
    def display_life_stage_flavor_text(self):
        flavor_texts = {
            LifeStage.EGG: ["The egg wiggles slightly.", "A soft tapping sound can be heard from the egg", "Soft sounds can be heard from the egg", "You can feel the egg vibrating from inside"],
            LifeStage.CHILD: [f"{self.name} is giggling happily to themselves.", f"{self.name} is courageously exploring their surroundings", f"A mischevious grin spreads across {self.name}'s face."],
            LifeStage.TEEN: [f"{self.name} is trying to do some dance moves.", f"You look over at {self.name} and see them trying to act cool.", f"{self.name} is singing some pop punk song to themselves"],
            LifeStage.ADULT: [f"{self.name} begins contemplating their lot in life.", f"You look over and see {self.name} balancing their checkbook.", f"{self.name} starts tidying up their surroundings."],
            LifeStage.MATURE: [f"You see {self.name} grumbling to themselves about aches and pains.", f"{self.name} is looking for a comfy place to sit.", f"You hear {self.name} yelling at some kids for playing ball in the street."],
            LifeStage.ELDER: [f"{self.name} moves slowly around the room, bones creaking, wheezing.", f"You notice {self.name} not moving... Nevermind, they were just sleeping.", f"{self.name} calls for you to bring them their pills."]
        }
        if self.life_stage in flavor_texts:
            available_texts = [text for text in flavor_texts[self.life_stage] if text != self.last_flavor_text]
            if available_texts:
                self.flavor_text = random.choice(available_texts)
            else:
                self.flavor_text = random.choice(flavor_texts[self.life_stage])
            self.last_flavor_text = self.flavor_text
        else:
            self.flavor_text = ''
        return self.flavor_text


    def display_need_based_messages(self):
        messages = []
        if self.hunger < 50:
            messages.append(f"{self.name}'s tummy starts tumbling... Maybe 'feed' them?")
        if self.thirst < 50:
            messages.append(f"{self.name}'s lips look parched... maybe 'water' them?")
        if self.sleep < 50:
            messages.append(f"{self.name}'s eyes look tired... Maybe 'tuckin' them?")
        if self.bladder < 50:
            messages.append(f"{self.name}'s does the potty dance... Maybe 'potty' them?")
        if self.hygiene < 50:
            messages.append(f"{self.name}'s smells disgusting... Maybe 'bathe' them?")
        if self.socialize < 50:
            messages.append(f"{self.name}'s so lonely and bored... Maybe 'play' with them?")

        if messages:
            new_need_message = random.choice(messages)
            if new_need_message != self.last_need_message:
                self.need_message = new_need_message
                self.last_need_message = new_need_message
            else:
                self.need_message = ''
        else:
            self.need_message = ''
        return self.need_message
        

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

