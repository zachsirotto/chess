from __future__ import annotations
from chess import Color, IntoSquareSet, Square
from typing import Dict, Iterable, Optional, Tuple, Union, List
import chess
import chess.svg
import xml.etree.ElementTree as ET
import math


def _board(board: Optional[chess.BaseBoard] = None, *,
           orientation: Color = chess.WHITE,
           lastmove: Optional[chess.Move] = None,
           check: Optional[List[Square]] = None,
           arrows: Iterable[Union[Arrow, Tuple[Square, Square]]] = [],
           squares: Optional[IntoSquareSet] = None,
           size: Optional[int] = None,
           coordinates: bool = True,
           colors: Dict[str, str] = {},
           flipped: bool = False,
           style: Optional[str] = None) -> str:
    """
    Renders a board with pieces and/or selected squares as an SVG image.

    :param board: A :class:`chess.BaseBoard` for a chessboard with pieces, or
        ``None`` (the default) for a chessboard without pieces.
    :param orientation: The point of view, defaulting to ``chess.WHITE``.
    :param lastmove: A :class:`chess.Move` to be highlighted.
    :param check: Squares to be marked indicating a check.
    :param arrows: A list of :class:`~chess.svg.Arrow` objects, like
        ``[chess.svg.Arrow(chess.E2, chess.E4)]``, or a list of tuples, like
        ``[(chess.E2, chess.E4)]``. An arrow from a square pointing to the same
        square is drawn as a circle, like ``[(chess.E2, chess.E2)]``.
    :param squares: A :class:`chess.SquareSet` with selected squares.
    :param size: The size of the image in pixels (e.g., ``400`` for a 400 by
        400 board), or ``None`` (the default) for no size limit.
    :param coordinates: Pass ``False`` to disable the coordinate margin.
    :param colors: A dictionary to override default colors. Possible keys are
        ``square light``, ``square dark``, ``square light lastmove``,
        ``square dark lastmove``, ``margin``, ``coord``, ``arrow green``,
        ``arrow blue``, ``arrow red``, and ``arrow yellow``. Values should look
        like ``#ffce9e`` (opaque), or ``#15781B80`` (transparent).
    :param flipped: Pass ``True`` to flip the board.
    :param style: A CSS stylesheet to include in the SVG image.

    >>> import chess
    >>> import chess.svg
    >>>
    >>> board = chess.Board("8/8/8/8/4N3/8/8/8 w - - 0 1")
    >>> squares = board.attacks(chess.E4)
    >>> chess.svg.board(board, squares=squares, size=350)  # doctest: +SKIP

    .. image:: ../docs/Ne4.svg
        :alt: 8/8/8/8/4N3/8/8/8

    .. deprecated:: 1.1
        Use *orientation* with a color instead of the *flipped* toggle.
    """
    orientation ^= flipped
    margin = 15 if coordinates else 0
    svg = chess.svg._svg(8 * chess.svg.SQUARE_SIZE + 2 * margin, size)

    if style:
        ET.SubElement(svg, "style").text = style

    defs = ET.SubElement(svg, "defs")
    if board:
        for piece_color in chess.COLORS:
            for piece_type in chess.PIECE_TYPES:
                if board.pieces_mask(piece_type, piece_color):
                    defs.append(ET.fromstring(
                        chess.svg.PIECES[chess.Piece(piece_type, piece_color).symbol()]))

    squares = chess.SquareSet(squares) if squares else chess.SquareSet()
    if squares:
        defs.append(ET.fromstring(XX))

    if check is not None:
        defs.append(ET.fromstring(chess.svg.CHECK_GRADIENT))

    if coordinates:
        margin_color, margin_opacity = chess.svg._color(colors, "margin")
        ET.SubElement(svg, "rect", chess.svg._attrs({
            "x": 0,
            "y": 0,
            "width": 2 * margin + 8 * chess.svg.SQUARE_SIZE,
            "height": 2 * margin + 8 * chess.svg.SQUARE_SIZE,
            "fill": margin_color,
            "opacity": margin_opacity if margin_opacity < 1.0 else None,
        }))

    for square, bb in enumerate(chess.BB_SQUARES):
        file_index = chess.square_file(square)
        rank_index = chess.square_rank(square)

        x = (file_index if orientation else 7 -
             file_index) * chess.svg.SQUARE_SIZE + margin
        y = (7 - rank_index if orientation else rank_index) * \
            chess.svg.SQUARE_SIZE + margin

        cls = ["square", "light" if chess.BB_LIGHT_SQUARES & bb else "dark"]
        if lastmove and square in [lastmove.from_square, lastmove.to_square]:
            cls.append("lastmove")
        fill_color, fill_opacity = chess.svg._color(colors, " ".join(cls))

        cls.append(chess.SQUARE_NAMES[square])

        ET.SubElement(svg, "rect", chess.svg._attrs({
            "x": x,
            "y": y,
            "width": chess.svg.SQUARE_SIZE,
            "height": chess.svg.SQUARE_SIZE,
            "class": " ".join(cls),
            "stroke": "none",
            "fill": fill_color,
            "opacity": fill_opacity if fill_opacity < 1.0 else None,
        }))

        if check and square in check:
            ET.SubElement(svg, "rect", chess.svg._attrs({
                "x": x,
                "y": y,
                "width": chess.svg.SQUARE_SIZE,
                "height": chess.svg.SQUARE_SIZE,
                "class": "check",
                "fill": "url(#check_gradient)",
            }))

        # Render pieces.
        if board is not None:
            piece = board.piece_at(square)
            if piece:
                ET.SubElement(svg, "use", {
                    "xlink:href": f"#{chess.COLOR_NAMES[piece.color]}-{chess.PIECE_NAMES[piece.piece_type]}",
                    "transform": f"translate({x:d}, {y:d})",
                })

        # Render selected squares.
        if squares is not None and square in squares:
            ET.SubElement(svg, "use", chess.svg._attrs({
                "xlink:href": "#xx",
                "x": x,
                "y": y,
            }))

    if coordinates:
        coord_color, coord_opacity = chess.svg._color(colors, "coord")
        for file_index, file_name in enumerate(chess.FILE_NAMES):
            x = (file_index if orientation else 7 -
                 file_index) * chess.svg.SQUARE_SIZE + margin
            svg.append(chess.svg._coord(file_name, x, 0, chess.svg.SQUARE_SIZE, margin,
                                        True, margin, color=coord_color, opacity=coord_opacity))
            svg.append(chess.svg._coord(file_name, x, margin + 8 * chess.svg.SQUARE_SIZE, chess.svg.SQUARE_SIZE,
                                        margin, True, margin, color=coord_color, opacity=coord_opacity))
        for rank_index, rank_name in enumerate(chess.RANK_NAMES):
            y = (7 - rank_index if orientation else rank_index) * \
                chess.svg.SQUARE_SIZE + margin
            svg.append(chess.svg._coord(rank_name, 0, y, margin, chess.svg.SQUARE_SIZE,
                                        False, margin, color=coord_color, opacity=coord_opacity))
            svg.append(chess.svg._coord(rank_name, margin + 8 * chess.svg.SQUARE_SIZE, y, margin,
                                        chess.svg.SQUARE_SIZE, False, margin, color=coord_color, opacity=coord_opacity))

    for arrow in arrows:
        try:
            tail, head, color = arrow.tail, arrow.head, arrow.color  # type: ignore
        except AttributeError:
            tail, head = arrow  # type: ignore
            color = "green"

        try:
            color, opacity = _color(colors, " ".join(["arrow", color]))
        except KeyError:
            opacity = 1.0

        tail_file = chess.square_file(tail)
        tail_rank = chess.square_rank(tail)
        head_file = chess.square_file(head)
        head_rank = chess.square_rank(head)

        xtail = margin + \
            (tail_file + 0.5 if orientation else 7.5 -
             tail_file) * chess.svg.SQUARE_SIZE
        ytail = margin + \
            (7.5 - tail_rank if orientation else tail_rank + 0.5) * \
            chess.svg.SQUARE_SIZE
        xhead = margin + \
            (head_file + 0.5 if orientation else 7.5 -
             head_file) * chess.svg.SQUARE_SIZE
        yhead = margin + \
            (7.5 - head_rank if orientation else head_rank + 0.5) * \
            chess.svg.SQUARE_SIZE

        if (head_file, head_rank) == (tail_file, tail_rank):
            ET.SubElement(svg, "circle", chess.svg._attrs({
                "cx": xhead,
                "cy": yhead,
                "r": chess.svg.SQUARE_SIZE * 0.9 / 2,
                "stroke-width": chess.svg.SQUARE_SIZE * 0.1,
                "stroke": color,
                "opacity": opacity if opacity < 1.0 else None,
                "fill": "none",
                "class": "circle",
            }))
        else:
            marker_size = 0.75 * chess.svg.SQUARE_SIZE
            marker_margin = 0.1 * chess.svg.SQUARE_SIZE

            dx, dy = xhead - xtail, yhead - ytail
            hypot = math.hypot(dx, dy)

            shaft_x = xhead - dx * (marker_size + marker_margin) / hypot
            shaft_y = yhead - dy * (marker_size + marker_margin) / hypot

            xtip = xhead - dx * marker_margin / hypot
            ytip = yhead - dy * marker_margin / hypot

            ET.SubElement(svg, "line", _attrs({
                "x1": xtail,
                "y1": ytail,
                "x2": shaft_x,
                "y2": shaft_y,
                "stroke": color,
                "opacity": opacity if opacity < 1.0 else None,
                "stroke-width": chess.svg.SQUARE_SIZE * 0.2,
                "stroke-linecap": "butt",
                "class": "arrow",
            }))

            marker = [(xtip, ytip),
                      (shaft_x + dy * 0.5 * marker_size / hypot,
                       shaft_y - dx * 0.5 * marker_size / hypot),
                      (shaft_x - dy * 0.5 * marker_size / hypot,
                       shaft_y + dx * 0.5 * marker_size / hypot)]

            ET.SubElement(svg, "polygon", _attrs({
                "points": " ".join(f"{x},{y}" for x, y in marker),
                "fill": color,
                "opacity": opacity if opacity < 1.0 else None,
                "class": "arrow",
            }))

    return chess.svg.SvgWrapper(ET.tostring(svg).decode("utf-8"))


chess.svg.board = _board
