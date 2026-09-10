from __future__ import annotations

import argparse
import logging
import time

from src.common.can_interface import CANInterface
from src.common.dbc_codec import DBCCodec
from src.common.logger_config import configure_logging
from src.common.message_definitions import SPEED_DATA
from src.nodes.dashboard_receiver.display_renderer import render


logger = logging.getLogger("DashboardECU")


def run(
    interface: str,
    timeout_ms: int,
) -> None:

    configure_logging()

    can_interface = CANInterface(interface)
    codec = DBCCodec()

    timeout_seconds = timeout_ms / 1000.0

    last_received = time.monotonic()

    logger.info(
        "Dashboard ECU started. Monitoring ID 0x%03X",
        SPEED_DATA.can_id,
    )

    try:

        while True:

            message = can_interface.recv(
                timeout=0.1
            )

            now = time.monotonic()

            if message is not None:

                if (
                    message.arbitration_id
                    != SPEED_DATA.can_id
                ):
                    continue

                if message.dlc != SPEED_DATA.dlc:

                    logger.error(
                        "Malformed SpeedData: "
                        "expected DLC=%d received DLC=%d",
                        SPEED_DATA.dlc,
                        message.dlc,
                    )

                    continue

                try:

                    decoded = codec.decode_frame(
                        message
                    )

                    speed = decoded["VehicleSpeed"]

                    last_received = now

                    render(speed)

                    logger.debug(
                        "RX speed=%.2f km/h",
                        speed,
                    )

                except Exception as exc:

                    logger.exception(
                        "Failed to decode SpeedData: %s",
                        exc,
                    )

            if (
                now - last_received
                > timeout_seconds
            ):

                logger.warning(
                    "SPEED DATA TIMEOUT: "
                    "no valid frame received for %.0f ms",
                    timeout_ms,
                )

                last_received = now

    except KeyboardInterrupt:

        logger.info("Dashboard stopping.")

    finally:

        print()

        can_interface.shutdown()


def main() -> None:

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--interface",
        default="vcan0",
    )

    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=500,
    )

    args = parser.parse_args()

    if args.timeout_ms <= 0:
        raise SystemExit(
            "timeout-ms must be greater than zero"
        )

    run(
        interface=args.interface,
        timeout_ms=args.timeout_ms,
    )


if __name__ == "__main__":
    main()
