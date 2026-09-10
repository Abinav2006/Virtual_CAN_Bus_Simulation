from __future__ import annotations

import logging
from typing import Optional

import can


class CANInterface:
    """Small abstraction around python-can."""

    def __init__(
        self,
        channel: str = "vcan0",
        receive_own_messages: bool = False,
    ) -> None:

        self.channel = channel

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

        self.bus = can.Bus(
            interface="socketcan",
            channel=channel,
            receive_own_messages=receive_own_messages,
        )

        self.logger.info(
            "Opened CAN interface %s",
            channel,
        )

    def send(self, message: can.Message) -> None:
        try:
            self.bus.send(message)

        except can.CanError as exc:
            self.logger.error(
                "CAN transmission failed: %s",
                exc,
            )
            raise

    def recv(
        self,
        timeout: Optional[float] = None,
    ) -> Optional[can.Message]:

        return self.bus.recv(timeout)

    def shutdown(self) -> None:

        self.logger.info(
            "Closing CAN interface %s",
            self.channel,
        )

        self.bus.shutdown()
