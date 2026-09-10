from dataclasses import dataclass


@dataclass(frozen=True)
class MessageSpec:
    name: str
    can_id: int
    dlc: int
    period_ms: int | None = None


SPEED_DATA = MessageSpec(
    name="SpeedData",
    can_id=0x100,
    dlc=8,
    period_ms=100,
)

BRAKE_DATA = MessageSpec(
    name="BrakeData",
    can_id=0x080,
    dlc=8,
    period_ms=50,
)

RPM_DATA = MessageSpec(
    name="RPMData",
    can_id=0x101,
    dlc=8,
    period_ms=100,
)
