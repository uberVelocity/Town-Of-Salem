import hello_world
import sys
from PySide2 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = hello_world.MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())