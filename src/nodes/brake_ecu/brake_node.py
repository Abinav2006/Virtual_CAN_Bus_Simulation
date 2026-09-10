from __future__ import annotations

import argparse
import time

import can

from src.common.can_interface import CANInterface
from src.common.dbc_codec import DBCCodec
from src.common.logger_config import configure_logging
from src.common.message_definitions import BRAKE_DATA


def run(interface: str, period_ms: int) -> None:

    configure_logging()

    can_interface = CANInterface(interface)
    codec = DBCCodec()

    pressure = 0.0

    try:

        while True:

            pressure += 1.0

            if pressure > 100.0:
                pressure = 0.0

            payload = codec.encode_brake_pressure(
                pressure
            )

            message = can.Message(
                arbitration_id=BRAKE_DATA.can_id,
                data=payload,
                is_extended_id=False,
            )

            can_interface.send(message)

            print(
                f"Brake ECU TX "
                f"ID=0x{BRAKE_DATA.can_id:03X} "
                f"pressure={pressure:.1f} bar"
            )

            time.sleep(
                period_ms / 1000.0
            )

    except KeyboardInterrupt:
        pass

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
        default=50,
    )

    args = parser.parse_args()

    run(
        args.interface,
        args.period_ms,
    )


if __name__ == "__main__":
    main()
