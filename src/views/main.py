import chess
import chess.svg
from math import floor
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.defaultSize = 500                  # size of chessboard
        self.squares = [[0] * 8] * 8
        self.setWindowTitle("chess")
        self.board = chess.Board()
        self.boardWidget = QSvgWidget(parent=self)
        self.currentPlayer = chess.WHITE
        self.sqSelected = None
        self.pieceSelected = None
        self.boardWidget.load(chess.svg.board(
            self.board, size=self.cbSize).encode('utf8'))
        self.boardWidget.setGeometry(0, 0, self.defaultSize, self.defaultSize)
        self.boardWidget.show()
        self.setCentralWidget(self.boardWidget)

    def changeTurns(self):
        self.currentPlayer = not self.currentPlayer

    def cbSize(self):
        return self.width(), self.height()

    def marginSize(self):
        cbWidth, cbHeight = self.cbSize()
        return floor(1/24 * cbWidth), floor(1/24 * cbHeight)

    def squareSize(self):
        cbWidth, cbHeight = self.cbSize()
        marginX, marginY = self.marginSize()
        squareWidth = (cbWidth - (2 * marginX)) / 8.0
        squareHeight = (cbHeight - (2 * marginY)) / 8.0
        return squareWidth, squareHeight

    def paintEvent(self, event):
        self.boardWidget.load(chess.svg.board(
            self.board, size=self.cbSize).encode("utf8"))

    def mousePressEvent(self, event):
        cbWidth, cbHeight = self.cbSize()
        sqWidth, sqHeight = self.squareSize()
        marginX, marginY = self.marginSize()
        if event.buttons() == Qt.LeftButton:
            if marginX <= event.x() <= cbWidth - marginX and marginY <= event.y() <= cbHeight - marginY:
                x = int((event.x() - marginX) / sqWidth)
                y = 7 - int((event.y() - marginY) / sqHeight)
                # chess.sqare.mirror() if white is on top
                # if sq already selected, make a move
                if self.sqSelected:
                    print("attempt to make move")
                    self.board.push(chess.Move(
                        from_square=self.sqSelected,
                        to_square=chess.square(x, y)  # ,
                        # promotion=self.pieceSelected
                    ))
                    self.sqSelected, pieceSelected = None, None
                    self.changeTurns()
                    self.update()
                # sq is not selected yet
                else:
                    # get square number
                    self.sqSelected = chess.square(x, y)
                    # if current player's piece is not on square, do not select piece
                    # if self.board.piece_at(square).belongsToCurrentPlayer():
                    # find and select square
                    self.pieceSelected = self.board.piece_at(self.sqSelected)
                print(x, y)
