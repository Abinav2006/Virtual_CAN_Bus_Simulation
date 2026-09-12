import can

from src.common.message_definitions import SPEED_DATA


def test_wrong_dlc_is_detectable():

    message = can.Message(
        arbitration_id=SPEED_DATA.can_id,
        data=[0x01, 0x02],
        is_extended_id=False,
    )

    assert message.dlc != SPEED_DATA.dlc


def test_unknown_id_is_not_speed_data():

    message = can.Message(
        arbitration_id=0x555,
        data=[0x00] * 8,
        is_extended_id=False,
    )

    assert (
        message.arbitration_id
        != SPEED_DATA.can_id
    )
