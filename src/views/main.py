import chess
import chess.svg
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget  # , QTabWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from .square import Square

svgX = 50                          # top left x-pos of chessboard
svgY = 50                          # top left y-pos of chessboard
cbSize = 600                       # size of chessboard
margin = 0.05 * cbSize
#  if self.coordinates == True else 0
squareSize = (cbSize - 2 * margin) / 8.0


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.squares = [[0] * 8] * 8
        self.setWindowTitle("chess")

        self.board = chess.Board()

        # self.mainWidget = QTabWidget(self)
        self.boardWidget = QSvgWidget(parent=self)
        self.grid = QWidget(parent=self)
        # self.grid.move(1, 1)
        # self.groupBox = QGroupBox('grid')
        self.createGrid()

        self.coordinates = True

        self.boardWidget.load(chess.svg.board(
            self.board, size=350).encode('utf8'))

        # self.boardWidget.setGeometry(100, 100, 759, 668)

        # self.setGeometry(300, 300, 800, 800)
        # self.grid.setGeometry(50, 50, cbSize, cbSize)
        self.boardWidget.setGeometry(svgX, svgY, cbSize, cbSize)
        # see chess.svg.py line 129

        self.boardWidget.show()

        # self.mainWidget.addTab(self.boardWidget, 'board')
        # self.mainWidget.addTab(self.grid, 'grid')

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(self.boardWidget)

    def createGrid(self):
        dimensions = self.geometry()
        # bt_w = dimensions.width() / 8 - dimensions.width() / 26
        # bt_h = dimensions.height() / 8 - dimensions.height() / 26
        layout = QGridLayout()
        layout.setGeometry(50, 50, cbSize, cbSize)
        # layout.setContentsMargins(0, 0, 0, 0)
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)
        for i in range(8):
            # layout.setRowMinimumHeight(i, squareSize)
            for j in range(8):
                self.squares[i][j] = Square(i * 8 + j, squareSize)
                # self.squares[i][j].setGeometry(bt_w * j, bt_h * i, bt_w, bt_h)
                layout.addWidget(self.squares[i][j], i, j)
        self.boardWidget.setLayout(layout)
        # windowLayout = QVBoxLayout()
        # windowLayout.addWidget(self.groupBox)
        # self.setLayout(windowLayout)

    def paintEvent(self, event):
        self.boardWidget.load(chess.svg.board(
            self.board, size=cbSize, coordinates=self.coordinates).encode("utf8"))
