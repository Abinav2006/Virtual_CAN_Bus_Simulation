from __future__ import annotations

import argparse
import logging
import time

import can

from src.common.can_interface import CANInterface
from src.common.dbc_codec import DBCCodec
from src.common.logger_config import configure_logging
from src.common.message_definitions import SPEED_DATA
from src.nodes.ecu_speed_sender.speed_generator import SpeedGenerator


logger = logging.getLogger("SpeedECU")


def run(
    interface: str,
    period_ms: int,
) -> None:

    configure_logging()

    can_interface = CANInterface(interface)
    codec = DBCCodec()
    generator = SpeedGenerator()

    period_seconds = period_ms / 1000.0

    logger.info(
        "Speed ECU started: CAN ID=0x%03X period=%dms",
        SPEED_DATA.can_id,
        period_ms,
    )

    try:

        next_transmission = time.monotonic()

        while True:

            speed = generator.next_speed()

            payload = codec.encode_speed(speed)

            message = can.Message(
                arbitration_id=SPEED_DATA.can_id,
                data=payload,
                is_extended_id=False,
            )

            can_interface.send(message)

            logger.info(
                "TX ID=0x%03X speed=%.2f km/h",
                message.arbitration_id,
                speed,
            )

            next_transmission += period_seconds

            sleep_time = (
                next_transmission - time.monotonic()
            )

            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                next_transmission = time.monotonic()

    except KeyboardInterrupt:

        logger.info("Speed ECU stopping.")

    finally:

        can_interface.shutdown()


def main() -> None:

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--interface",
        default="vcan0",
    )

    parser.add_argument(
        "--period-ms",
        type=int,
        default=100,
    )

    args = parser.parse_args()

    if args.period_ms <= 0:
        raise SystemExit(
            "period-ms must be greater than zero"
        )

    run(
        interface=args.interface,
        period_ms=args.period_ms,
    )


if __name__ == "__main__":
    main()
