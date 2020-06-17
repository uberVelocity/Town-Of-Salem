import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui

class Sim(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Define GUI widgets
        self.start_button = QtWidgets.QPushButton("Start")
        
        self.title = QtWidgets.QLabel("Town of Salem")
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.vote_text = QtWidgets.QLabel("Voting strategy:")
        self.runs_text = QtWidgets.QLabel("Runs:")

        self.dropdown_strategy = QtWidgets.QComboBox()
        self.dropdown_strategy.addItem("RANDOM")
        self.dropdown_strategy.addItem("KNOWLEDGE")

        self.runs = QtWidgets.QLineEdit()

        # Define layout
        self.layout = QtWidgets.QFormLayout()
        
        # Add widgets to layout
        self.layout.addWidget(self.title)
        self.layout.addRow(self.vote_text, self.dropdown_strategy)
        self.layout.addRow(self.runs_text, self.runs)
        self.layout.addWidget(self.start_button)
        
        # Set layout to main window
        self.setLayout(self.layout)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Sim()
    widget.resize(400, 400)
    widget.show()

    sys.exit(app.exec_())
    pass