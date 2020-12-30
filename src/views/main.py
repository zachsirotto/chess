import chess
import chess.svg
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget  # , QTabWidget
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QCursor
from .square import Square

svgX = 50                          # top left x-pos of chessboard
svgY = 50                          # top left y-pos of chessboard
cbSize = 600                       # size of chessboard


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.margin = 0.025 * cbSize
        self.squareSize = (cbSize - 2 * self.margin) / 8.0
        self.squares = [[0] * 8] * 8
        self.setWindowTitle("chess")
        self.board = chess.Board()
        self.boardWidget = QSvgWidget(parent=self)
        self.grid = QWidget(parent=self.boardWidget)
        self.grid.setGeometry(QRect(self.margin, self.margin, cbSize, cbSize))
        self.createGrid()
        self.coordinates = True
        self.boardWidget.load(chess.svg.board(
            self.board, size=cbSize).encode('utf8'))
        self.boardWidget.setGeometry(svgX, svgY, cbSize, cbSize)
        self.boardWidget.show()

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(self.grid)

    def createGrid(self):
        dimensions = self.geometry()
        # bt_w = dimensions.width() / 8 - dimensions.width() / 26
        # bt_h = dimensions.height() / 8 - dimensions.height() / 26
        layout = QGridLayout()
        # layout.setGeometry(QRect(svgx, svgY, cbSize, cbSize))
        # layout.setContentsMargins(0, 0, 0, 0)
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)
        for i in range(8):
            # layout.setRowMinimumHeight(i, squareSize)
            for j in range(8):
                self.squares[i][j] = Square(i * 8 + j, self.squareSize)
                # self.squares[i][j].setGeometry(bt_w * j, bt_h * i, bt_w, bt_h)
                layout.addWidget(self.squares[i][j], i, j)
        self.grid.setLayout(layout)
        # windowLayout = QVBoxLayout()
        # windowLayout.addWidget(self.groupBox)
        # self.setLayout(windowLayout)

    def paintEvent(self, event):
        self.boardWidget.load(chess.svg.board(
            self.board, size=cbSize, coordinates=self.coordinates).encode("utf8"))
