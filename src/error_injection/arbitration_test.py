from __future__ import annotations

import can


HIGH_PRIORITY_ID = 0x080
LOW_PRIORITY_ID = 0x100


def compare_priority(
    first_id: int,
    second_id: int,
) -> int:

    if first_id < second_id:
        return first_id

    return second_id


def run_arbitration_test() -> None:

    winner = compare_priority(
        HIGH_PRIORITY_ID,
        LOW_PRIORITY_ID,
    )

    print(
        f"CAN ID 0x{HIGH_PRIORITY_ID:03X} "
        f"vs 0x{LOW_PRIORITY_ID:03X}"
    )

    print(
        f"Expected arbitration winner: "
        f"0x{winner:03X}"
    )


if __name__ == "__main__":
    run_arbitration_test()
