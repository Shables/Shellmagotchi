        

## Redundant by different approach
#Create a horizontal Layout for each need
#        h_layout = QHBoxLayout()
#        h_layout.addWidget(label)
#        h_layout.addWidget(progress_bar)
#        h_layout.addStretch()
#
#        self.stats_layout.addWidget(progress_bar, i // 3, i % 3)


## Redundant with update_ui function
#    def update_progress_bars(self):
#        if self.gotchi:
#            print("game window update needs")
#            self.gotchi.update_needs()
#            print("game window udpated needs")
#            for need, bar in self.progress_bars.items():
#                value = getattr(self.gotchi, need)
#                bar.setValue(value)

## Can't figure out where to put these damn signals and slots
# I dont know of any better way to get the rebirth function from shellmagotchi.py
# to connect to the game_window.py module.. so.. more signals and slots
#        if self.gotchi:
#            self.gotchi.rebirthRequested.connect(self.handle_rebirth_request)




## I believe this code is redundant.. but maybe not
#            # Reset UI Is this needed???
#            self.info_frame.clear()
#            for bar in self.progress_bars.values():
#                bar.setValue(100)
#            self.happiness_bar.setValue(100)
#            self.update_character_image()
#            self.input_box.clear()
#
#            # Send signal for new main_loop (may not be necessary)
#            self.gotchiCreated.emit(self.gotchi)
        