from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path

import can


def capture(
    interface: str,
    output: Path,
    duration: float,
) -> None:

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    bus = can.Bus(
        interface="socketcan",
        channel=interface,
    )

    with output.open(
        "w",
        newline="",
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "timestamp",
                "can_id",
                "dlc",
                "data",
            ]
        )

        end = (
            time.monotonic()
            + duration
        )

        while time.monotonic() < end:

            message = bus.recv(
                timeout=0.1
            )

            if message is None:
                continue

            writer.writerow(
                [
                    message.timestamp,
                    hex(message.arbitration_id),
                    message.dlc,
                    message.data.hex().upper(),
                ]
            )

    bus.shutdown()


def main() -> None:

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--interface",
        default="vcan0",
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--duration",
        type=float,
        default=10.0,
    )

    args = parser.parse_args()

    capture(
        args.interface,
        args.output,
        args.duration,
    )


if __name__ == "__main__":
    main()
