# Scenario 23 - Dots and Boxes

## Changes made

The original modular structure is preserved:
- `board.py` stores lines, completed boxes, board dimensions, and rendering.
- `rules.py` parses and validates player commands.
- `game.py` owns turn order, scores, and game-over state.
- `main.py` handles interactive configuration and the CLI.

### Task 1 - Bug investigation and fix

The starter implementation mixed the state transition directly into the interactive loop. A move had to be validated, applied, compared with the previous completed-box set, scored, and used to decide the next player.

The fix centralizes that transition in `DotsAndBoxes.play_move()`:

1. Reject the move before changing state if the game is finished or the line is invalid.
2. Add the line through the board module.
3. Capture exactly the newly completed boxes returned by the board.
4. Award those boxes to the current player.
5. Keep the same player when at least one box was completed; otherwise switch players.
6. Mark the game finished when every board line has been played.

This makes the score/turn rule deterministic and directly testable.

### Task 2 - Meaningful gameplay feature

The game now supports **configurable board dimensions**.

At startup, players can choose the number of rows and columns instead of being locked to a fixed 2 x 2 board. The same board, rule, score, and turn logic works for the selected size.

Custom player names were also added so the configured game is easier to follow during play.

### Task 3 - Validation and robustness

The program safely rejects:
- malformed commands;
- non-numeric or negative coordinates;
- invalid orientations;
- coordinates outside the selected board;
- repeated lines;
- moves after the board is complete.

Rejected input never changes the board, score, or current player.

The interactive loop also supports `Q` to end a game cleanly.

### Task 4 - Automated testing

`test_dots_and_boxes.py` covers:
- valid horizontal move;
- valid vertical move;
- repeated/invalid move;
- box completion and extra turn;
- end-of-game condition;
- post-game move rejection;
- malformed commands;
- invalid coordinates/orientation;
- move parsing.

## Run the game

```text
python main.py
```

Example moves:

```text
H 0 0
V 0 0
H 1 0
V 0 1
```

Rows and columns start at zero.

## Run the tests

```text
python -m unittest -v
```

No third-party dependencies are required.

## Video checklist

**Before changes:** capture a 10-second clip of the original starter project before applying these changes. The visible starter code already appears to retain the same player after a completed box, so do not fabricate a broken state; capture the actual baseline behaviour from your local copy and describe the observed issue during review.

**After changes:** capture a 10-second clip showing a box being scored, the same player receiving the extra turn, and the new configurable board size/name setup.

## Design decisions

The board remains responsible for geometry, the rules module remains responsible for command validation, and the game module remains responsible for state transitions. This avoids putting gameplay logic into `main.py` and keeps the implementation easy to unit test.
