from src.common.message_definitions import (
    BRAKE_DATA,
    RPM_DATA,
    SPEED_DATA,
)


def test_speed_message_definition():

    assert SPEED_DATA.can_id == 0x100
    assert SPEED_DATA.dlc == 8
    assert SPEED_DATA.period_ms == 100


def test_brake_has_higher_priority():

    assert (
        BRAKE_DATA.can_id
        < SPEED_DATA.can_id
    )


def test_rpm_message_definition():

    assert RPM_DATA.can_id == 0x101
    assert RPM_DATA.dlc == 8
