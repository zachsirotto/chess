import chess
import chess.svg
from src.controllers import click
from math import floor
from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import (
    QMainWindow,
    QToolButton,
    QAction,
    QMenuBar,
    QMenu,
    QToolBar,
    QPlainTextEdit
)
from PyQt5.QtGui import QCursor, QIcon


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.MOVE_LIST_SIZE = 95
        self.TOOLBAR_SIZE = 20
        self.defaultSize = 500
        self.squares = [[0] * 8] * 8
        self.setWindowTitle("chess")
        self.board = chess.Board()
        self.boardWidget = QSvgWidget(parent=self)
        self.currentPlayer = chess.WHITE
        self.sqSelected = None
        self.pieceSelected = None
        self.lastMove = None
        self.checkSquares = []
        self.boardWidget.load(chess.svg.board(
            self.board, size=self.cbSize).encode('utf8'))
        self.boardWidget.setGeometry(0, 0, self.defaultSize, self.defaultSize)
        self.boardWidget.show()

        # add menu bar
        self.menuBar = QMenuBar()
        self.__initMenu()

        # add toolbars
        # self.toolBar = QToolBar()
        self.rightToolBar = QToolBar()
        self.__initToolbar()

        # init move list
        self.__initMoveList()

        # set board as central widget for resizing
        self.setCentralWidget(self.boardWidget)

    def __initMenu(self):
        self.menuBar.setNativeMenuBar(True)
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction("New")
        self.menuBar.addMenu(self.fileMenu)
        self.setMenuBar(self.menuBar)

    def __initToolbar(self):
        # init top toolbar
        # self.toolBar.setMovable(False)
        # toolButton = QToolButton()
        # toolButton.setText("Apple")
        # toolButton.setCheckable(True)
        # toolButton.setAutoExclusive(True)
        # self.toolBar.setFixedHeight(self.TOOLBAR_SIZE)
        # self.toolBar.addWidget(toolButton)
        # self.addToolBar(self.toolBar)
        # init right toolbar
        self.rightToolBar.setOrientation(Qt.Vertical)
        self.rightToolBar.setMovable(False)
        self.rightToolBar.setFixedWidth(self.MOVE_LIST_SIZE)
        self.addToolBar(Qt.RightToolBarArea, self.rightToolBar)

    def __initMoveList(self):
        self.moveList = QPlainTextEdit()
        self.moveList.setCursorWidth(0)
        self.moveList.setPlaceholderText('No moves yet')
        self.moveList.setReadOnly(True)
        self.rightToolBar.addWidget(self.moveList)

    def changeTurns(self):
        self.currentPlayer = not self.currentPlayer

    # currently returns window size, will have to change if we add a toolbar
    def cbSize(self):
        return self.width() - self.MOVE_LIST_SIZE, self.height()  # - self.TOOLBAR_SIZE

    def marginSize(self):
        cbWidth, cbHeight = self.cbSize()
        return floor(1/24 * cbWidth), floor(1/24 * cbHeight)

    def getSquareAndPiece(self, x, y):
        square = chess.square(x, y)
        piece = self.board.piece_at(square)
        return square, piece

    def setSquareAndPiece(self, square, piece):
        self.sqSelected = square
        # self.pieceSelected = self.board.piece_at(
        #     self.sqSelected)
        self.update()

    def squareSize(self):
        cbWidth, cbHeight = self.cbSize()
        marginX, marginY = self.marginSize()
        squareWidth = (cbWidth - (2 * marginX)) / 8.0
        squareHeight = (cbHeight - (2 * marginY)) / 8.0
        return squareWidth, squareHeight

    def getRankAndFile(self, event):
        sqWidth, sqHeight = self.squareSize()
        marginX, marginY = self.marginSize()
        file = int((event.x() - marginX) / sqWidth)
        rank = 7 - int((event.y() - marginY) / sqHeight)
        return file, rank

    def paintEvent(self, event):
        self.boardWidget.load(chess.svg.board(
            self.board,
            size=self.cbSize,
            lastmove=self.lastMove,
            check=self.checkSquares,
            squares=chess.SquareSet.from_square(
                self.sqSelected) if self.sqSelected else chess.SquareSet()  # ,
            # selected=self.sqSelected  # ,
            # colors={
            #     'square light lastmove': '#ffce9e99',
            #     'square dark lastmove': '#d18b4799'
            # }
        ).encode("utf8"))

    def onBoard(self, event):
        cbWidth, cbHeight = self.cbSize()
        marginX, marginY = self.marginSize()
        onX = (marginX <= event.x() <= cbWidth - marginX)
        onY = (marginY <= event.y() <= cbHeight - marginY)
        return onX and onY

    def mousePressEvent(self, event):
        click.mouseClick(self, event)
