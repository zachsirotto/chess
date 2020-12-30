import chess
import chess.svg
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget  # , QTabWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from .square import Square


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.squares = [[0] * 8] * 8
        self.setWindowTitle("chess")

        self.board = chess.Board()

        squares = self.board.attacks(chess.E4)

        # self.mainWidget = QTabWidget(self)
        self.boardWidget = QSvgWidget()
        self.grid = QWidget(self)
        self.grid.move(1, 1)
        # self.groupBox = QGroupBox('grid')
        self.createGrid()

        self.boardWidget.load(bytearray(chess.svg.board(
            self.board, squares=squares, size=350), 'utf8'))

        self.boardWidget.setGeometry(50, 50, 759, 668)
        self.boardWidget.show()

        # label = QLabel("chess window")

        # # The `Qt` namespace has a lot of attributes to customise
        # # widgets. See: http://doc.qt.io/qt-5/qt.html
        # label.setAlignment(Qt.AlignCenter)

        # self.mainWidget.addTab(self.boardWidget, 'board')
        # self.mainWidget.addTab(self.grid, 'grid')

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(self.boardWidget)

    def createGrid(self):
        dimensions = self.geometry()
        bt_w = dimensions.width() / 8 - dimensions.width() / 26
        bt_h = dimensions.height() / 8 - dimensions.height() / 26
        layout = QGridLayout()
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)
        for i in range(8):
            for j in range(8):
                self.squares[i][j] = Square(i * 8 + j)
                self.squares[i][j].setGeometry(bt_w * j, bt_h * i, bt_w, bt_h)
                layout.addWidget(self.squares[i][j], i, j)
        self.boardWidget.setLayout(layout)
        # windowLayout = QVBoxLayout()
        # windowLayout.addWidget(self.groupBox)
        # self.setLayout(windowLayout)

    def mouse_clicked(self, QMouseEvent):
        # https://doc.qt.io/qt-5/qmouseevent.html
        pos = QMouseEvent.pos()
        # https://doc.qt.io/qt-5/qrect.html
        # dimensions = self.geometry()
        # x = (pos.x() - (dimensions.width() / 8 / 4))
        # y = (pos.y() - (dimensions.height() / 8 / 4))
        # x = (dimensions.width() / 8) % pos.x()
        # y = (dimensions.height() / 8) % pos.y()
        # print(x, y)
        # print(dimensions.width() / 8 - dimensions.width() / 8 / 3)
        # print(pos)
