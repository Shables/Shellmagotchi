import sys
import traceback
import time
import random
from save_system import delete_save, load_game
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QInputDialog,
                               QHBoxLayout, QFrame, QTextEdit, QLineEdit, QProgressBar, QGridLayout, QLabel)
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import Qt, QTimer, Signal, QObject, Slot, QPropertyAnimation, QPoint, QEasingCurve
from shellmagotchi import Shellmagotchi


color_red = QColor(255, 0, 0)  # TODO: The rest of the colors

class ShellmagotchiGame(QMainWindow):
    gotchiCreated = Signal(Shellmagotchi) # Signal Defined
    updateUISignal = Signal()

    def __init__(self, gotchi=None, debug=False):
        super().__init__()
        self.gotchi = gotchi
        self.init_ui()
        self.updateUISignal.connect(self._update_ui) # maybe self._update_ui
        self.waiting_for_rebirth_name = False
        self.debug = debug
        self.animation = None
        self.last_animation_time = 0
        self.animation_cooldown = 10

        if not self.gotchi:
            save_data, _ = load_game()
            if save_data:
                self.gotchi = Shellmagotchi(save_data["name"])
                self.connect_gotchi_signals()
                self.show_all_ui_elements()
                self.update_ui()
            else:
                self.add_info("Woah! You found an egg!")
                self.add_info("What would you like to name it?")
        else:
            self.connect_gotchi_signals()
            self.show_all_ui_elements()
            self.update_ui()

    def show_all_ui_elements(self):
        self.happiness_bar.setVisible(True)
        self.happiness_label.setVisible(True)
        self.life_stage_label.setVisible(True)
        self.name_label.setVisible(True)
        self.character_label.setVisible(True)
        self.stats_frame.setVisible(True)

    # Signal Handling
    def connect_gotchi_signals(self):
        if self.gotchi:
            self.gotchi.rebirthRequested.connect(self.handle_rebirth_request)
            self.gotchi.died.connect(self.update_ui)

    def disconnect_gotchi_signals(self):
        if self.gotchi:
            try:
                self.gotchi.rebirthRequested.disconnect(self.handle_rebirth_request)
                self.gotchi.died.disconnect(self.update_ui)
            except TypeError:
                print("Warning: Failed to disconnect a signal, likely none connected")
    # GUI
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
        
        # Changes aa0
        self.character_layout = QGridLayout(self.character_frame) # Moved from scary changes
        self.character_label = QLabel(self.character_frame)
        self.character_label.setAlignment(Qt.AlignCenter)
        self.character_layout.addWidget(self.character_label, 0, 0, alignment=Qt.AlignCenter)

        # Scary Changes aa0
    
        #self.character_label = QLabel()
        #self.character_layout.addWidget(self.character_label, 0, 0, 2, 1, alignment=Qt.AlignCenter)
       
        # Display life stage, after initialized
        self.life_stage_label = QLabel()
        self.life_stage_label.setStyleSheet("color: grey;")
        self.life_stage_label.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self.character_layout.addWidget(self.life_stage_label, 1, 0, alignment=Qt.AlignBottom | Qt.AlignRight)
        self.life_stage_label.setVisible(False)

        # Display name, after initialized
        self.name_label = QLabel()
        self.name_label.setStyleSheet("color: grey;")
        self.name_label.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        self.character_layout.addWidget(self.name_label, 1, 0, alignment=Qt.AlignBottom | Qt.AlignLeft)
        self.name_label.setVisible(False)

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
        
        # Hide the character image and stats at start
        self.character_label.setVisible(False)
        self.stats_frame.setVisible(False)
        self.happiness_bar.setVisible(False)
        self.happiness_label.setVisible(False)

    def _update_ui(self):
        if self.debug:
            print("update_ui() called from ShellmagotchiGame class")
        if self.gotchi:
            for need, bar in self.progress_bars.items():
                value = getattr(self.gotchi, need)
                bar.setValue(value)

            self.happiness_bar.setValue(int(self.gotchi.happiness))
            self.life_stage_label.setText(self.gotchi.life_stage.value)
            self.name_label.setText(self.gotchi.name)

            self.character_label.setVisible(self.gotchi.alive and not self.gotchi.runaway) # Show gotchi image when alive
            self.update_terminal()
            self.central_widget.layout().update()
            self.update_character_image()


    def update_ui(self):
            self.updateUISignal.emit()

    @Slot()
    def handle_rebirth_request(self):
        if not self.waiting_for_rebirth_name:
            self.waiting_for_rebirth_name = True
            self.disconnect_gotchi_signals()
            if self.debug:
                print("HANDLE REBIRTH REQUEST() TRIGGERED")
            self.add_info("Wait... something's happening")
            self.add_info(f"You see an egg sitting in the ashes of {self.gotchi.name}")
            self.add_info(f"I ... guess you should name it?.. what would you like to name it?")
            self.input_box.setPlaceholderText("Enter new Gotchi name...")

    def process_command(self):
        command = self.input_box.text().strip().lower()
        self.input_box.clear()

        if self.waiting_for_rebirth_name:
            self.complete_rebirth(command)
        elif not self.gotchi:
            self.create_initial_gotchi(command)
        else:
            self.handle_regular_command(command)

    def complete_rebirth(self, new_name):
        if new_name:
            delete_save()
            new_gotchi = Shellmagotchi(new_name)
            self.gotchi = new_gotchi
            self.connect_gotchi_signals()
            self.gotchiCreated.emit(self.gotchi)     
            self.add_info(f"Take good care of {self.gotchi.name}!")
            self.update_ui()
            self.waiting_for_rebirth_name = False
            self.input_box.setPlaceholderText("Enter command...")
        else:
            self.add_info("Please enter a valid name for your new Gotchi.")
    
    def create_initial_gotchi(self, name):
        if name and not self.gotchi:
            self.gotchi = Shellmagotchi(name)
            self.gotchi.game = self
            self.connect_gotchi_signals()
            self.gotchiCreated.emit(self.gotchi)
            self.add_info(f"Take good care of {name}!")
            self.update_ui()

            self.show_all_ui_elements()
            self.update_character_image()
            self.update_ui()
            
    def handle_regular_command(self, command):
        if not self.gotchi:
            print("Something wrong with handle_regular_command method")
        elif self.gotchi and not self.gotchi.rebirthing: # Only Handle These Commands when Gotchi is True
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
            elif command == 'rebirth':
                self.add_info("Are you sure you would like to rebirth?")
                self.add_info("Rebirthing will archive the current gotchi and spawn a new egg")
                self.add_info("Confirm? (Y/N): ")
                if command == 'y':
                    self.update_ui()
                    self.gotchi.rebirth()
                elif command == 'n':
                    self.add_info("Cancelling rebirth...")
                else:
                    self.add_info("Unknown command")
            else:
                self.add_info("Unknown command")
        elif self.gotchi and not self.gotchi.rebirthing:
            return command

    def update_character_image(self):
        if self.gotchi:
            image_path = f"assets/{self.gotchi.life_stage.value}.png"
            pixmap = QPixmap(image_path)
        if not pixmap.isNull() and pixmap is not None:
            self.character_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            animation_current_time = time.time() * 1000 # Convert to milliseconds
            if animation_current_time - self.last_animation_time > self.animation_cooldown:
                self.animate_character()
                self.last_animation_time = animation_current_time       
        else:
            print(f"Image not found: {image_path}")
    
    def animate_character(self):
        print("Attempting to animate character")
        if str(self.gotchi.life_stage.value).lower() == "egg":
            self.animate_egg()
            print("sent egg animations")
        else:
            animation_type = random.choice(["move", "jump", "flip"])
            if animation_type == "move":
                self.animate_move()
            elif animation_type == "jump":
                self.animate_jump()
            elif animation_type == "flip":
                self.animate_flip()
            print("sent animation calls")

    def animate_egg(self):
        animation = QPropertyAnimation(self.character_label, b'pos')
        animation.setDuration(1000)
        start_pos = self.character_label.pos()
        animation.setStartValue(start_pos)
        animation.setKeyValueAt(0.25, start_pos + QPoint(10, 0))
        animation.setKeyValueAt(0.75, start_pos + QPoint(-10, 0))
        animation.setEndValue(start_pos)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()
        print("Egg animation started")

    def animate_move(self):
        animation = QPropertyAnimation(self.character_label, b'pos')
        animation.setDuration(1000)
        start_pos = self.character_label.pos()
        end_pos = start_pos + QPoint(random.choice([-50, 50]), 0)
        animation.setStartValue(start_pos)
        animation.setEndValue(end_pos)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()

    def animate_jump(self):
        animation = QPropertyAnimation(self.character_label, b'pos')
        animation.setDuration(500)
        start_pos = self.character_label.pos()
        animation.setStartValue(start_pos)
        animation.setKeyValueAt(0.5, start_pos + QPoint(0, -30))
        animation.setEndValue(start_pos)
        animation.setEasingCurve(QEasingCurve.OutInQuad)
        animation.start()

    def animate_flip(self):
        animation = QPropertyAnimation(self.character_label, b'geometry')
        animation.setDuration(500)
        start_geometry = self.character_label.geometry()
        animation.setStartValue(start_geometry)

        mid_geometry = start_geometry
        mid_geometry.setWidth(1)

        end_geometry = start_geometry

        animation.setKeyValueAt(0.5, mid_geometry)
        animation.setEndValue(end_geometry)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()
                                
    def add_info(self, text):
        self.info_frame.append(text)
        
    def update_terminal(self): 
        if self.gotchi:    
            info = f"Current Needs -- Hunger: {self.gotchi.hunger:.2f}, Thirst: {self.gotchi.thirst:.2f}, "
            info += f"Sleep: {self.gotchi.sleep:.2f}, Hygiene: {self.gotchi.hygiene:.2f}, "
            info += f"Bladder: {self.gotchi.bladder:.2f}, Socialize: {self.gotchi.socialize:.2f}"

            self.add_info(info)

