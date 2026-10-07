import unittest

from game import DotsAndBoxes
from rules import parse_move, valid_move


class TestDotsAndBoxes(unittest.TestCase):
    def test_valid_horizontal_move(self):
        game = DotsAndBoxes()
        result = game.play_move("H", 0, 0)
        self.assertTrue(result["valid"])
        self.assertTrue(game.board.horizontal[0][0])
        self.assertEqual(game.current, 1)

    def test_valid_vertical_move(self):
        game = DotsAndBoxes()
        result = game.play_move("V", 0, 0)
        self.assertTrue(result["valid"])
        self.assertTrue(game.board.vertical[0][0])
        self.assertEqual(game.current, 1)

    def test_repeated_move_is_rejected_without_state_change(self):
        game = DotsAndBoxes()
        self.assertTrue(game.play_move("H", 0, 0)["valid"])
        scores_before = game.scores[:]
        current_before = game.current
        result = game.play_move("H", 0, 0)
        self.assertFalse(result["valid"])
        self.assertEqual(result["reason"], "invalid_move")
        self.assertEqual(game.scores, scores_before)
        self.assertEqual(game.current, current_before)
        self.assertEqual(game.board.line_count(), 1)

    def test_completion_scores_box_and_keeps_turn(self):
        game = DotsAndBoxes()
        game.play_move("H", 0, 0)
        game.play_move("H", 1, 0)
        game.play_move("V", 0, 0)
        result = game.play_move("V", 0, 1)
        self.assertTrue(result["valid"])
        self.assertEqual(result["completed"], 1)
        self.assertEqual(game.scores, [0, 1])
        self.assertEqual(game.current, 1)

    def test_end_of_game_condition_and_post_game_rejection(self):
        game = DotsAndBoxes(rows=1, cols=1)
        for move in [("H", 0, 0), ("H", 1, 0), ("V", 0, 0), ("V", 0, 1)]:
            game.play_move(*move)

        self.assertTrue(game.finished)
        self.assertTrue(game.board.is_complete())
        self.assertEqual(sum(game.scores), 1)

        scores_before = game.scores[:]
        lines_before = game.board.line_count()
        result = game.play_move("H", 0, 0)
        self.assertFalse(result["valid"])
        self.assertEqual(result["reason"], "game_over")
        self.assertEqual(game.scores, scores_before)
        self.assertEqual(game.board.line_count(), lines_before)

    def test_malformed_command_is_rejected(self):
        game = DotsAndBoxes()
        self.assertEqual(game.play_command("banana")["reason"], "format")
        self.assertEqual(game.play_command("H x 0")["reason"], "format")
        self.assertEqual(game.play_command("V -1 0")["reason"], "format")

    def test_out_of_range_and_invalid_orientation_are_rejected(self):
        game = DotsAndBoxes()
        self.assertFalse(valid_move(game.board, "H", 99, 99))
        self.assertFalse(game.play_command("V 99 99")["valid"])
        self.assertFalse(game.play_command("X 0 0")["valid"])

    def test_parse_move_normalizes_valid_input(self):
        self.assertEqual(parse_move(" h 1 0 "), ("H", 1, 0))


if __name__ == "__main__":
    unittest.main()
