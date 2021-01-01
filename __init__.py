import sys
import src.patches.board
from PyQt5.QtWidgets import QApplication
from src.views.main import MainWindow


app = QApplication([])

window = MainWindow()
window.show()

app.exec_()
