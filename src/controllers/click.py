import chess
import chess.svg
from PyQt5.QtCore import Qt, QRect, QPoint


def mouseClick(self, event):
    if event.buttons() in [Qt.LeftButton, Qt.RightButton]:
        if self.onBoard(event):
            # chess.sqare.mirror() if white is on top
            file, rank = self.getRankAndFile(event)
            # if sq already selected
            if self.sqSelected is not None:
                # reselect piece if necessary
                square, piece = self.getSquareAndPiece(file, rank)
                if piece and piece.color == self.currentPlayer:
                    self.setSquareAndPiece(square, piece)
                    return
                # make a move
                move = chess.Move(
                    from_square=self.sqSelected,
                    to_square=square
                )
                # determine if move is a promotion
                if self.board.piece_type_at(self.sqSelected) == chess.PAWN and rank in [0, 7] and not move.promotion:
                    self.promotionWindow.show()
                    # TODO: listen for selection, then promote piece
                    move = chess.Move(
                        move.from_square,
                        move.to_square,
                        chess.QUEEN
                    )
                # if move is legal
                if move in self.board.legal_moves:
                    # make move
                    self.updateMoveList(move)
                    self.board.push(move)
                    self.sqSelected, self.pieceSelected = None, None
                    self.changeTurns()
                    self.lastMove = move
                    # get check squares if move puts king in check
                    if self.board.is_check():
                        self.checkSquares = self.board.checkers()
                        self.checkSquares.add(
                            self.board.king(self.currentPlayer))
                    else:
                        self.checkSquares = []
                    self.update()
            # sq is not selected yet
            else:
                square, piece = self.getSquareAndPiece(file, rank)
                if piece and piece.color == self.currentPlayer:
                    self.setSquareAndPiece(square, piece)
