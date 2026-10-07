def valid_move(board, orientation, row, col):
    """Return True only for an unused line inside the board."""
    if orientation not in {"H", "V"}:
        return False
    if not isinstance(row, int) or not isinstance(col, int):
        return False

    if orientation == "H":
        return 0 <= row <= board.rows and 0 <= col < board.cols and not board.horizontal[row][col]

    return 0 <= row < board.rows and 0 <= col <= board.cols and not board.vertical[row][col]


def completed_boxes(board, before):
    return len(board.completed - before)


def parse_move(raw):
    """Parse H row col or V row col. Return None when malformed."""
    if not isinstance(raw, str):
        return None
    parts = raw.strip().upper().split()
    if len(parts) != 3:
        return None

    orientation, row_text, col_text = parts
    if orientation not in {"H", "V"}:
        return None

    try:
        row, col = int(row_text), int(col_text)
    except ValueError:
        return None

    if row < 0 or col < 0:
        return None
    return orientation, row, col
