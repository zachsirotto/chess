import chess
import chess.svg
from src.controllers import click
from src.views.promotion import MyPopup
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
    QTextEdit
)
from PyQt5.QtGui import QCursor, QIcon, QKeySequence


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
        self.promotionWindow = MyPopup()
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
        self.moveList = QTextEdit()
        self.__initMoveList()

        # set board as central widget for resizing
        self.setCentralWidget(self.boardWidget)

    def __initMenu(self):
        self.menuBar.setNativeMenuBar(True)
        self.fileMenu = QMenu("&File")
        self.fileMenu.addAction("New")
        self.fileMenu.addAction("Save")
        self.fileMenu.addAction("Load")
        self.menuBar.addMenu(self.fileMenu)
        self.gameMenu = QMenu("&Game")
        self.undoAction = QAction("Undo")
        self.undoAction.setShortcut(QKeySequence("CTRL+Z"))
        self.undoAction.triggered.connect(self.undoMove)
        self.gameMenu.addAction(self.undoAction)
        self.menuBar.addMenu(self.gameMenu)
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
        self.moveList.setCursorWidth(0)
        self.moveList.setFontPointSize(16)
        self.moveList.setPlaceholderText('No moves yet')
        self.moveList.setAlignment(Qt.AlignCenter)
        self.moveList.setReadOnly(True)
        self.rightToolBar.addWidget(self.moveList)

    def changeTurns(self):
        self.currentPlayer = not self.currentPlayer
        self.board.turn = self.currentPlayer

    # currently returns window size, will have to change if we add a toolbar
    def cbSize(self):
        return self.width() - self.MOVE_LIST_SIZE, self.height()  # - self.TOOLBAR_SIZE

    def marginSize(self):
        cbWidth, cbHeight = self.cbSize()
        return floor(1/24 * cbWidth), floor(1/24 * cbHeight)

    def undoMove(self):
        try:
            self.board.pop()
        except IndexError as _:
            return  # no moves have been made yet
        self.moveList.undo()
        self.moveList.setAlignment(Qt.AlignCenter)
        self.changeTurns()
        self.lastMove = self.board.peek() if self.board.move_stack else None
        self.moveList.ensureCursorVisible()
        self.setSquareAndPiece(None, None)

    def getSquareAndPiece(self, x, y):
        square = chess.square(x, y)
        piece = self.board.piece_at(square)
        return square, piece

    def setSquareAndPiece(self, square, piece):
        self.sqSelected = square
        self.pieceSelected = piece
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

    def getMoveText(self, move, piece):
        uci = move.uci()
        return '{} {} — {}'.format(
            piece.unicode_symbol(invert_color=True),
            uci[:2],
            uci[2:]
        )

    def updateMoveList(self, move):
        moveText = self.getMoveText(
            move, self.board.piece_at(move.from_square))
        self.moveList.insertPlainText('{}\n'.format(moveText))
        self.moveList.ensureCursorVisible()

    def paintEvent(self, event):
        self.boardWidget.load(chess.svg.board(
            self.board,
            size=self.cbSize,
            lastmove=self.lastMove,
            check=self.checkSquares,
            squares=chess.SquareSet.from_square(
                self.sqSelected) if self.sqSelected is not None else chess.SquareSet()  # ,
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
