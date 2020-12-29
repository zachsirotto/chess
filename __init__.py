import chess
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


board = chess.Board()

app = QApplication([])

window = QMainWindow()
window.show()

app.exec_()
