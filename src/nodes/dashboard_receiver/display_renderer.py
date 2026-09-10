from __future__ import annotations


def render(speed_kph: float) -> None:

    bar_width = 40

    normalized = min(
        speed_kph / 120.0,
        1.0,
    )

    filled = int(
        normalized * bar_width
    )

    bar = (
        "#" * filled
        + "-" * (bar_width - filled)
    )

    print(
        f"\rSpeed: {speed_kph:6.2f} km/h "
        f"[{bar}]",
        end="",
        flush=True,
    )
