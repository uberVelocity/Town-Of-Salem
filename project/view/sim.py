import sys
import random
import subprocess
import os
import run_params

from PySide2 import QtCore, QtWidgets, QtGui

class Sim(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        """Define GUI widgets"""
        
        # Start button of simulation
        self.start_button = QtWidgets.QPushButton("Start")
        
        # Title of GUI
        self.title = QtWidgets.QLabel("Town of Salem")
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        # Text labels
        self.action_text = QtWidgets.QLabel("Action strategy:")
        self.vote_text = QtWidgets.QLabel("Voting strategy:")
        self.runs_text = QtWidgets.QLabel("Runs:")
        self.interactions_text = QtWidgets.QLabel("Interactions:")

        # Agent strategy when voting
        self.dropdown_vote = QtWidgets.QComboBox()
        self.dropdown_vote.addItem("RANDOM")
        self.dropdown_vote.addItem("KNOWLEDGE")

        # Agent strategy when doing an action
        self.dropdown_action = QtWidgets.QComboBox()
        self.dropdown_action.addItem("RANDOM")
        self.dropdown_action.addItem("KNOWLEDGE")

        # Simulation display interactions between agent
        self.dropdown_interactions = QtWidgets.QComboBox()
        self.dropdown_interactions.addItem("OFF")
        self.dropdown_interactions.addItem("ON")

        # Number of runs input field
        self.runs = QtWidgets.QLineEdit()

        # Define layout
        self.layout = QtWidgets.QFormLayout()
        
        """Add widgets to layout"""
        # Add title to GUI
        self.layout.addWidget(self.title)

        # Add dropdowns to GUI
        self.layout.addRow(self.action_text, self.dropdown_action)
        self.layout.addRow(self.vote_text, self.dropdown_vote)
        self.layout.addRow(self.interactions_text, self.dropdown_interactions)
        
        # Add input fields to GUI
        self.layout.addRow(self.runs_text, self.runs)
        
        # Add buttons to GUI
        self.layout.addWidget(self.start_button)
        
        # Set layout to main window
        self.setLayout(self.layout)

        self.start_button.clicked.connect(self.start)

    # Starts the simulation with given parameters
    def start(self):

        # Change directory to location of main.py
        os.chdir("../")

        # Sets number of runs
        runs = run_params.runs
        if self.runs.text() != "":
            runs = self.runs.text()

        # Set interaction mode
        interactions = run_params.interactions
        if self.dropdown_interactions.currentIndex():
            interactions = True

        # Run the simulation as a subprocess
        if interactions:
            list_files = subprocess.run(["python3", "main.py", str(runs), "1"])
        else:
            list_files = subprocess.run(["python3", "main.py", str(runs)])
        print("The exit code was: %d" % list_files.returncode)
        
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Sim()
    widget.resize(400, 400)
    widget.show()

    sys.exit(app.exec_())
    pass