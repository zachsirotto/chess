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
        self.setCentralWidget(self.boardWidget)

    def changeTurns(self):
        self.currentPlayer = not self.currentPlayer

    def cbSize(self):
        return self.width(), self.height()

    def marginSize(self):
        cbWidth, cbHeight = self.cbSize()
        return floor(1/24 * cbWidth), floor(1/24 * cbHeight)

    def getSquareAndPiece(self, x, y):
        square = chess.square(x, y)
        piece = self.board.piece_at(square)
        return square, piece

    def setSquareAndPiece(self, square):
        self.sqSelected = square
        self.pieceSelected = self.board.piece_at(
            self.sqSelected)

    def squareSize(self):
        cbWidth, cbHeight = self.cbSize()
        marginX, marginY = self.marginSize()
        squareWidth = (cbWidth - (2 * marginX)) / 8.0
        squareHeight = (cbHeight - (2 * marginY)) / 8.0
        return squareWidth, squareHeight

    def getRankAndFile(self, event):
        file = int((event.x() - marginX) / sqWidth)
        rank = 7 - int((event.y() - marginY) / sqHeight)
        return file, rank

    def paintEvent(self, event):
        self.boardWidget.load(chess.svg.board(
            self.board,
            size=self.cbSize,
            lastmove=self.lastMove,
            check=self.checkSquares
        ).encode("utf8"))

    def mousePressEvent(self, event):
        cbWidth, cbHeight = self.cbSize()
        sqWidth, sqHeight = self.squareSize()
        marginX, marginY = self.marginSize()
        if event.buttons() == Qt.LeftButton:
            if marginX <= event.x() <= cbWidth - marginX and marginY <= event.y() <= cbHeight - marginY:
                file, rank = self.getRankAndFile(self, event)
                # chess.sqare.mirror() if white is on top
                # if sq already selected, make a move
                if self.sqSelected:
                    # reselect piece if necessary
                    square, piece = self.getSquareAndPiece(file, rank)
                    if piece and piece.color == self.currentPlayer:
                        self.setSquareAndPiece(square)
                        return
                    move = chess.Move(
                        from_square=self.sqSelected,
                        to_square=square  # ,
                        # promotion=self.pieceSelected
                    )
                    # if move is legal
                    if move in self.board.legal_moves:
                        self.board.push(move)
                        self.sqSelected, pieceSelected = None, None
                        self.changeTurns()
                        self.lastMove = move
                        # get check squares if move puts king in check
                        if self.board.is_check():
                            self.checkSquares = self.board.checkers()
                        else:
                            self.checkSquares = []
                        self.update()
                # sq is not selected yet
                else:
                    square, piece = self.getSquareAndPiece(file, rank)
                    # only select current player's pieces
                    if piece and piece.color == self.currentPlayer:
                        self.setSquareAndPiece(square)
                print(file, rank)
