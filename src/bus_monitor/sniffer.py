from __future__ import annotations

import argparse
import logging
from pathlib import Path

import can


logger = logging.getLogger("CANSniffer")


def capture(
    interface: str,
    output_path: Path,
    duration: float,
) -> None:

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    bus = can.Bus(
        interface="socketcan",
        channel=interface,
    )

    logger.info(
        "Capturing CAN traffic from %s",
        interface,
    )

    logger.info(
        "Output: %s",
        output_path,
    )

    writer = can.Logger(
        str(output_path)
    )

    listener = can.Logger(
        str(output_path)
    )

    del writer
    del listener

    notifier = can.Notifier(
        bus,
        [
            can.Logger(
                str(output_path)
            )
        ],
    )

    try:

        import time

        end_time = (
            time.monotonic()
            + duration
        )

        while time.monotonic() < end_time:
            time.sleep(0.1)

    except KeyboardInterrupt:

        logger.info("Capture interrupted.")

    finally:

        notifier.stop()
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

    logging.basicConfig(
        level=logging.INFO
    )

    capture(
        args.interface,
        args.output,
        args.duration,
    )


if __name__ == "__main__":
    main()
