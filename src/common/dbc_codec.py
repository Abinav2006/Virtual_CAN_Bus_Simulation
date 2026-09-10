from __future__ import annotations

from pathlib import Path
from typing import Any

import cantools
import can


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DBC_PATH = PROJECT_ROOT / "dbc" / "vehicle_network.dbc"


class DBCCodec:
    """Encode and decode CAN frames using the project DBC."""

    def __init__(self, dbc_path: Path = DBC_PATH) -> None:
        if not dbc_path.exists():
            raise FileNotFoundError(
                f"DBC file not found: {dbc_path}"
            )

        self.db = cantools.database.load_file(str(dbc_path))

    def encode_speed(self, speed_kph: float) -> bytes:
        """Encode vehicle speed into a SpeedData payload."""

        if not 0 <= speed_kph <= 655.35:
            raise ValueError(
                f"Speed out of range: {speed_kph}"
            )

        message = self.db.get_message_by_name("SpeedData")

        return message.encode(
            {
                "VehicleSpeed": speed_kph
            }
        )

    def decode_frame(self, message: can.Message) -> dict[str, Any]:
        """Decode a CAN message into a dictionary."""

        db_message = self.db.get_message_by_frame_id(
            message.arbitration_id
        )

        return db_message.decode(message.data)

    def encode_brake_pressure(self, pressure_bar: float) -> bytes:
        """Encode brake pressure."""

        if not 0 <= pressure_bar <= 6553.5:
            raise ValueError(
                f"Brake pressure out of range: {pressure_bar}"
            )

        message = self.db.get_message_by_name("BrakeData")

        return message.encode(
            {
                "BrakePressure": pressure_bar
            }
        )
