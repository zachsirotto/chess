import chess
import chess.svg
from PyQt5.QtCore import Qt


def mouseClick(main, event):
    if event.buttons() == Qt.LeftButton:
        if main.onBoard(event):
            # chess.sqare.mirror() if white is on top
            file, rank = main.getRankAndFile(event)
            # if sq already selected, make a move
            if main.sqSelected:
                # reselect piece if necessary
                square, piece = main.getSquareAndPiece(file, rank)
                if piece and piece.color == main.currentPlayer:
                    main.setSquareAndPiece(square)
                    return
                move = chess.Move(
                    from_square=main.sqSelected,
                    to_square=square  # ,
                    # promotion=main.pieceSelected
                )
                # if move is legal
                if move in main.board.legal_moves:
                    main.board.push(move)
                    main.sqSelected, pieceSelected = None, None
                    main.changeTurns()
                    main.lastMove = move
                    # get check squares if move puts king in check
                    if main.board.is_check():
                        main.checkSquares = main.board.checkers()
                    else:
                        main.checkSquares = []
                    main.update()
            # sq is not selected yet
            else:
                square, piece = main.getSquareAndPiece(file, rank)
                # only select current player's pieces
                if piece and piece.color == main.currentPlayer:
                    main.setSquareAndPiece(square)
