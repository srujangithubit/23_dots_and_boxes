from board import Board
from rules import parse_move, valid_move


class DotsAndBoxes:
    """Coordinates board state, turns, scores, and game completion."""

    def __init__(self, rows=2, cols=2, players=None):
        self.board = Board(rows, cols)
        self.players = list(players) if players else ["P1", "P2"]
        if len(self.players) != 2 or any(not name.strip() for name in self.players):
            raise ValueError("exactly two non-empty player names are required")
        self.current = 0
        self.scores = [0, 0]
        self.finished = False

    def play_move(self, orientation, row, col):
        if isinstance(orientation, str):
            orientation = orientation.upper()

        if self.finished or self.board.is_complete():
            self.finished = True
            return {"valid": False, "reason": "game_over", "completed": 0}

        if not valid_move(self.board, orientation, row, col):
            return {"valid": False, "reason": "invalid_move", "completed": 0}

        completed = self.board.add_line(orientation, row, col)
        count = len(completed)

        if count:
            self.scores[self.current] += count
        else:
            self.current = 1 - self.current

        self.finished = self.board.is_complete()
        return {
            "valid": True,
            "reason": "ok",
            "completed": count,
            "extra_turn": count > 0,
            "game_over": self.finished,
        }

    def play_command(self, raw):
        parsed = parse_move(raw)
        if parsed is None:
            return {"valid": False, "reason": "format", "completed": 0}
        return self.play_move(*parsed)

    def run(self):
        print("Dots and Boxes")
        print("Enter moves as H row col or V row col.")
        print("Rows and columns start at 0.")
        print("Complete a box to score and play again.")
        print("Enter Q to quit.")

        while not self.finished:
            self.board.display(self.scores, self.current, self.players)
            raw = input(f"{self.players[self.current]}, move: ").strip()

            if raw.upper() == "Q":
                print("Game ended by player.")
                return

            result = self.play_command(raw)
            if not result["valid"]:
                if result["reason"] == "format":
                    print("Invalid format. Use H row col or V row col.")
                elif result["reason"] == "game_over":
                    print("The board is already complete.")
                else:
                    print("Invalid or already-used move.")
                continue

            if result["completed"]:
                print(
                    f"{self.players[self.current]} completed "
                    f"{result['completed']} box(es) and plays again."
                )

        self.board.display(self.scores, self.current, self.players)
        print("Game over!")
        if self.scores[0] == self.scores[1]:
            print("The game is a draw.")
        else:
            winner = 0 if self.scores[0] > self.scores[1] else 1
            print(f"{self.players[winner]} wins!")
