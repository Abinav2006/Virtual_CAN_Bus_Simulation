from __future__ import annotations

import argparse
import logging

import can

from src.common.can_interface import CANInterface
from src.common.logger_config import configure_logging


logger = logging.getLogger("FaultInjector")


def inject_wrong_dlc(interface: str) -> None:

    bus = CANInterface(interface)

    try:

        message = can.Message(
            arbitration_id=0x100,
            data=[0x01, 0x02],
            is_extended_id=False,
        )

        logger.warning(
            "Injecting wrong DLC: ID=0x100 DLC=%d",
            message.dlc,
        )

        bus.send(message)

    finally:

        bus.shutdown()


def inject_unknown_id(interface: str) -> None:

    bus = CANInterface(interface)

    try:

        message = can.Message(
            arbitration_id=0x555,
            data=[0xAA] * 8,
            is_extended_id=False,
        )

        logger.warning(
            "Injecting unknown ID: 0x555"
        )

        bus.send(message)

    finally:

        bus.shutdown()


def main() -> None:

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--interface",
        default="vcan0",
    )

    parser.add_argument(
        "--fault",
        required=True,
        choices=[
            "wrong-dlc",
            "unknown-id",
        ],
    )

    args = parser.parse_args()

    configure_logging()

    if args.fault == "wrong-dlc":
        inject_wrong_dlc(args.interface)

    elif args.fault == "unknown-id":
        inject_unknown_id(args.interface)


if __name__ == "__main__":
    main()
