        

## Redundant by different approach
#Create a horizontal Layout for each need
        h_layout = QHBoxLayout()
        h_layout.addWidget(label)
        h_layout.addWidget(progress_bar)
        h_layout.addStretch()

        self.stats_layout.addWidget(progress_bar, i // 3, i % 3)
