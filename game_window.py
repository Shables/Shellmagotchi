import sys
import time
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                                QHBoxLayout, QFrame, QTextEdit, QLineEdit, QProgressBar, QGridLayout)
from PySide6.QtCore import Qt, QTimer
from shellmagotchi import Shellmagotchi

class ShellmagotchiGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shellmagotchi")
        self.setGeometry(100, 100, 600, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Top frame for Gotchi
        self.character_frame = QFrame()
        self.character_frame.setFrameShape(QFrame.Box)
        self.character_frame.setFixedHeight(200)
        self.layout.addWidget(self.character_frame)

        # Bottom frame for game information
        self.info_frame = QTextEdit()
        self.info_frame.setReadOnly(True)
        self.layout.addWidget(self.info_frame, stretch=2)

        # Input box at the very bottom
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter Command...")
        self.input_box.returnPressed.connect(self.process_command)
        self.layout.addWidget(self.input_box)

        # Initialize Shellmagotchi
        self.gotchi = Shellmagotchi("tester")

        # Stats display
        self.stats_frame = QFrame()
        self.stats_layout = QGridLayout(self.stats_frame)
        self.progress_bars = {}

        needs = ['hunger', 'thirst', 'sleep', 'hygiene', 'bladder', 'socialize']
        for i, need in enumerate(needs):
            progress_bar = QProgressBar()
            progress_bar.setTextVisible(True)
            progress_bar.setFormat(f"{need.capitalize()}: %p%")
            self.progress_bars[need] = progress_bar
            self.stats_layout.addWidget(progress_bar, i // 3, i % 3)
        
        self.layout.addWidget(self.stats_frame)

        # Set up timer for updating stats
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_stats)
        self.update_timer.start(5000) # Every 5 seconds

    def update_stats(self):
        self.gotchi.update_needs()
        for need, bar in self.progress_bars.items():
            value = getattr(self.gotchi, need)
            bar.setValue(value)


    def process_command(self):
        user_input = self.input_box.text().strip().lower()
        self.input_box.clear()


        if user_input == 'feed':
            self.gotchi.feed()
        elif user_input == 'water':
            self.gotchi.give_water()
        elif user_input == 'bathe':
            self.gotchi.bathe()
        elif user_input == 'tuck-in':
            self.gotchi.tuck_in()
        elif user_input == 'potty':
            self.gotchi.potty()
        elif user_input == 'socialize':
            self.gotchi.social()
        else:
            self.add_info("Unknown Command")
        
        self.update_info()

    def add_info(self, text):
        self.info_frame.append(text)

    def update_info(self):
        self.gotchi.update_needs()
        info = f"Current Needs -  -- Hunger: {self.gotchi.hunger}, Thirst: {self.gotchi.thirst}, "
        info += f"Sleep: {self.gotchi.sleep}, Hygiene: {self.gotchi.hygiene}, "
        info += f"Bladder: {self.gotchi.bladder}, Socialize: {self.gotchi.socialize}"
        self.add_info(info)


        