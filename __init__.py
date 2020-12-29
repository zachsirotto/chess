import sys
from PyQt5.QtWidgets import QApplication
from src.views.main import MainWindow


app = QApplication([])

window = MainWindow()
window.show()

app.exec_()
