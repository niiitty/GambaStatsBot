_SLOT_MACHINE_WIN_VALUES = {
    1: ("bar", "bar", "bar"),
    22: ("grape", "grape", "grape"),
    43: ("lemon", "lemon", "lemon"),
    64: ("seven", "seven", "seven"),
}


def _is_win(roll_value: int) -> bool:
    """Check if roll is winning."""
    return roll_value in _SLOT_MACHINE_WIN_VALUES

def _handle_win() -> None:
    print("WIN!!!")

def _handle_loss() -> None:
    print("LOSS :(")

def handle_result(roll_value) -> None:
    if _is_win(roll_value):
        _handle_win()
    else:
        _handle_loss()
