import sys
import traceback
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QFrame, QTextEdit, QLineEdit, QProgressBar, QGridLayout, QLabel)
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import Qt, QTimer, Signal
from shellmagotchi import Shellmagotchi

color_red = QColor(255, 0, 0)  # TODO: The rest of the colors

class ShellmagotchiGame(QMainWindow):
    gotchiCreated = Signal(Shellmagotchi) # Signal Defined
    def __init__(self, gotchi=None):
        super().__init__()
        self.gotchi = gotchi
        self.init_ui()
        #self.update_ui() # Updated right after initialization

    def init_ui(self):
        self.setWindowTitle("Tamagotchi Game")
        self.setGeometry(100, 100, 800, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Top 2/7: Character display
        self.character_frame = QFrame()
        self.character_frame.setFrameShape(QFrame.Box)
        self.character_frame.setFixedHeight(150)
        self.character_layout = QVBoxLayout(self.character_frame)
        self.character_label = QLabel()
        self.character_layout.addStretch()
        #self.character_label.setContentsMargins(10, 10, 10, 10)
        #pixmap = QPixmap("assets/egg.png")
        #self.character_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.character_layout.addWidget(self.character_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.character_frame)

        # Middle 1/7: Needs bars
        self.stats_frame = QFrame()
        self.stats_layout = QGridLayout(self.stats_frame)
        self.progress_bars = {}
        needs = ['hunger', 'thirst', 'sleep', 'hygiene', 'bladder', 'socialize']
        bar_colors = [color_red, QColor(0, 255, 0), QColor(0, 0, 255), QColor(255, 255, 0), QColor(255, 165, 0), QColor(255, 192, 203)]
        
        for i, need in enumerate(needs):
            label = QLabel(f"{need.capitalize()}:")
            progress_bar = QProgressBar()
            progress_bar.setTextVisible(True)
            progress_bar.setFixedWidth(300)
            progress_bar.setStyleSheet(f"QProgressBar::chunk {{background-color: {bar_colors[i].name()}; }}")

            self.progress_bars[need] = progress_bar

            row = i // 3
            col = i % 3
            self.stats_layout.addWidget(label, row, col * 2)
            self.stats_layout.addWidget(progress_bar, row, col * 2 + 1)
       
        # Happiness Display
        self.happiness_label = QLabel("Happiness:")
        self.happiness_label.setVisible(False)
        self.happiness_bar = QProgressBar()
        self.happiness_bar.setTextVisible(True)
        self.happiness_bar.setStyleSheet("QProgressBar::chunk {background-color: #FFFF00; }") # Yellow?


        self.layout.addWidget(self.happiness_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.happiness_bar)
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

        # Set up timer for updating stats
#        self.update_timer = QTimer(self)
#        self.update_timer.timeout.connect(self.update_ui) # Changed from self.update_progress_bars
#        self.update_timer.start(500)  # Update every 5 seconds

        # Timer for updating the terminal
#        self.update_terminal_timer = QTimer(self)
#        self.update_terminal_timer.timeout.connect(self.update_terminal)
#        self.update_terminal_timer.start(1000)


        # Display life stage, after initialized
        self.life_stage_label = QLabel()
        self.life_stage_label.setStyleSheet("color: grey;")
        self.life_stage_label.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self.character_layout.addWidget(self.life_stage_label, alignment=Qt.AlignBottom | Qt.AlignRight)
        self.life_stage_label.setVisible(False)

        self.add_info("Woah! You found an egg!")
        self.add_info("What would you like to name it?")
        
        # Hide the character image and stats at start
        self.character_label.setVisible(False)
        self.stats_frame.setVisible(False)
        self.happiness_bar.setVisible(False)
        self.happiness_label.setVisible(False)

    def update_ui(self):
        if self.gotchi:
            for need, bar in self.progress_bars.items():
                value = getattr(self.gotchi, need)
                bar.setValue(value)

            self.happiness_bar.setValue(int(self.gotchi.happiness))
            self.life_stage_label.setText(self.gotchi.life_stage)

            self.character_label.setVisible(self.gotchi.alive and not self.gotchi.runaway) # Show gotchi image when alive
            self.update_terminal()

    def process_command(self):
        command = self.input_box.text().strip().lower()
        self.input_box.clear()
       
        if not self.gotchi:
            name = command.strip().title()
            if name:
                self.gotchi = Shellmagotchi(name)
                self.gotchiCreated.emit(self.gotchi) # Emit signal when gotchi named and created
                self.add_info(f"Take good care of {name}!")

                self.happiness_bar.setVisible(True)
                self.happiness_label.setVisible(True)
                self.life_stage_label.setVisible(True)
                self.character_label.setVisible(True)
                self.stats_frame.setVisible(True)
                self.update_character_image()
                self.update_ui()
                

        elif self.gotchi: # Only Handle These Commands when Gotchi is True
            if command in ['feed', 'food', 'breakfast', 'lunch', 'dinner', 'snack']:
                self.gotchi.feed()
            elif command in ['water', 'drink', 'thirst', 'give water']:
                self.gotchi.give_water()
            elif command in ['bathe', 'wash', 'bath', 'shower']:
                self.gotchi.bathe()
            elif command in ['bedtime', 'tuckin', 'tuck-in', 'sleepy']:
                self.gotchi.tuck_in()
            elif command in ['potty', 'bathroom', 'pee']:
                self.gotchi.potty()
            elif command in ['socialize', 'play']:
                self.gotchi.social()
            else:
                self.add_info("Unknown command")

    def update_character_image(self):
        if self.gotchi:
            pixmap = QPixmap(f"assets/{self.gotchi.life_stage.lower()}.png")
            self.character_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def add_info(self, text):
        self.info_frame.append(text)
    
    def update_terminal(self):
        print("update_terminal called")    
        traceback.print_stack()   
        if self.gotchi:    
            info = f"Current Needs -- Hunger: {self.gotchi.hunger:.2f}, Thirst: {self.gotchi.thirst:.2f}, "
            info += f"Sleep: {self.gotchi.sleep:.2f}, Hygiene: {self.gotchi.hygiene:.2f}, "
            info += f"Bladder: {self.gotchi.bladder:.2f}, Socialize: {self.gotchi.socialize:.2f}"

            self.add_info(info)

