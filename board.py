class Board:
    """Stores the physical state of a Dots and Boxes board."""

    def __init__(self, rows=2, cols=2):
        if not isinstance(rows, int) or not isinstance(cols, int):
            raise ValueError("rows and cols must be integers")
        if rows < 1 or cols < 1:
            raise ValueError("rows and cols must be at least 1")
        self.rows = rows
        self.cols = cols
        self.horizontal = [[False] * cols for _ in range(rows + 1)]
        self.vertical = [[False] * (cols + 1) for _ in range(rows)]
        self.completed = set()

    def add_line(self, orientation, row, col):
        """Add a legal line and return boxes completed by that line."""
        if orientation == "H":
            self.horizontal[row][col] = True
        elif orientation == "V":
            self.vertical[row][col] = True
        else:
            raise ValueError("orientation must be H or V")

        before = set(self.completed)
        self._update_completed()
        return self.completed - before

    def _update_completed(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (
                    self.horizontal[r][c]
                    and self.horizontal[r + 1][c]
                    and self.vertical[r][c]
                    and self.vertical[r][c + 1]
                ):
                    self.completed.add((r, c))

    def is_complete(self):
        return self.line_count() == self.total_lines()

    def line_count(self):
        return sum(map(sum, self.horizontal)) + sum(map(sum, self.vertical))

    def total_lines(self):
        return self.rows * (self.cols + 1) + self.cols * (self.rows + 1)

    def display(self, scores, current, players=None):
        names = players or ["P1", "P2"]
        print()
        print(f"Scores: {names[0]}={scores[0]}  {names[1]}={scores[1]} | Turn: {names[current]}")

        for r in range(self.rows + 1):
            print(".".join("---" if self.horizontal[r][c] else "   " for c in range(self.cols)))
            if r < self.rows:
                middle = []
                for c in range(self.cols + 1):
                    middle.append("|" if self.vertical[r][c] else " ")
                    if c < self.cols:
                        middle.append(" " + ("X" if (r, c) in self.completed else " ") + " ")
                print("".join(middle))
        print()
