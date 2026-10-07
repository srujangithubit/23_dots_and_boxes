from game import DotsAndBoxes


def get_positive_int(prompt, default):
    raw = input(prompt).strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        print(f"Invalid number. Using {default}.")
        return default
    if value < 1:
        print(f"Number must be at least 1. Using {default}.")
        return default
    return value


if __name__ == "__main__":
    print("Dots and Boxes")
    print("Configure the board, or press Enter to use the default 2 x 2 board.")
    rows = get_positive_int("Rows [2]: ", 2)
    cols = get_positive_int("Columns [2]: ", 2)
    p1 = input("Player 1 name [P1]: ").strip() or "P1"
    p2 = input("Player 2 name [P2]: ").strip() or "P2"
    DotsAndBoxes(rows, cols, [p1, p2]).run()
