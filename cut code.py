        

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
 