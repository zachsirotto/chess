import chess
import chess.svg
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QMainWindow  # QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

# Subclass QMainWindow to customise your application's main window


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("chess")

        board = chess.Board()

        squares = board.attacks(chess.E4)

        boardSvg = QSvgWidget()
        boardSvg.load(bytearray(chess.svg.board(
            board, squares=squares, size=350), 'utf8'))

        boardSvg.setGeometry(50, 50, 759, 668)
        boardSvg.show()

        # label = QLabel("chess window")

        # # The `Qt` namespace has a lot of attributes to customise
        # # widgets. See: http://doc.qt.io/qt-5/qt.html
        # label.setAlignment(Qt.AlignCenter)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(boardSvg)

    def mousePressEvent(self, QMouseEvent):
        print(QMouseEvent.pos())

    def mouseReleaseEvent(self, QMouseEvent):
        cursor = QCursor()
        print(cursor.pos())
