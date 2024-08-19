import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QFrame, QTextEdit, QLineEdit, QProgressBar, QGridLayout, QLabel)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer
from shellmagotchi import Shellmagotchi

class ShellmagotchiGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tamagotchi Game")
        self.setGeometry(100, 100, 600, 700)  # Increased height to accommodate all elements

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Top 2/7: Character display
        self.character_frame = QFrame()
        self.character_frame.setFrameShape(QFrame.Box)
        self.character_frame.setFixedHeight(150)
        self.character_layout = QVBoxLayout(self.character_frame)
        self.character_label = QLabel()
        pixmap = QPixmap("assets/egg.png")
        self.character_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.character_layout.addWidget(self.character_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.character_frame)

        # Middle 1/7: Needs bars
        self.stats_frame = QFrame()
        self.stats_layout = QGridLayout(self.stats_frame)
        self.progress_bars = {}
        needs = ['hunger', 'thirst', 'sleep', 'hygiene', 'bladder', 'socialize']
        for i, need in enumerate(needs):
            label = QLabel(f"{need.capitalize()}:")
            progress_bar = QProgressBar()
            progress_bar.setTextVisible(True)
            progress_bar.setFixedWidth(200)
            self.progress_bars[need] = progress_bar

            #Create a horizontal Layout for each need
            h_layout = QHBoxLayout()
            h_layout.addWidget(label)
            h_layout.addWidget(progress_bar)
            h_layout.addStretch()

            self.stats_layout.addWidget(progress_bar, i // 3, i % 3)

        self.stats_layout.setColumnStretch(0, 1)
        self.stats_layout.setColumnStretch(1, 1)
        self.stats_layout.setColumnStretch(2, 1)        
        self.layout.addWidget(self.stats_frame)

        # Bottom 4/7: Game information
        self.info_frame = QTextEdit()
        self.info_frame.setReadOnly(True)
        self.layout.addWidget(self.info_frame, stretch=4)

        # Input box at the very bottom
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter command...")
        self.input_box.returnPressed.connect(self.process_command)
        self.layout.addWidget(self.input_box)

        # Initialize Shellmagotchi
        self.gotchi = Shellmagotchi("Tester")

        # Set up timer for updating stats
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_progress_bars)
        self.update_timer.start(500)  # Update every 5 seconds

        # Timer for updating the terminal
        self.update_terminal_timer = QTimer(self)
        self.update_terminal_timer.timeout.connect(self.update_terminal)
        self.update_terminal_timer.start(10000)

    def process_command(self):
        command = self.input_box.text().strip().lower()
        self.input_box.clear()

        if command == 'feed':
            self.gotchi.feed()
        elif command == 'water':
            self.gotchi.give_water()
        elif command == 'bathe':
            self.gotchi.bathe()
        elif command == 'bedtime':
            self.gotchi.tuck_in()
        elif command == 'potty':
            self.gotchi.potty()
        elif command in ['socialize', 'play']:
            self.gotchi.social()
        else:
            self.add_info("Unknown command")

        self.update_progress_bars()
        self.update_terminal()

    def add_info(self, text):
        self.info_frame.append(text)

    def update_progress_bars(self):
        self.gotchi.update_needs()
        for need, bar in self.progress_bars.items():
            value = getattr(self.gotchi, need)
            bar.setValue(value)

    def update_terminal(self):        
        info = f"Current Needs -- Hunger: {self.gotchi.hunger}, Thirst: {self.gotchi.thirst}, "
        info += f"Sleep: {self.gotchi.sleep}, Hygiene: {self.gotchi.hygiene}, "
        info += f"Bladder: {self.gotchi.bladder}, Socialize: {self.gotchi.socialize}"

        self.add_info(info)

