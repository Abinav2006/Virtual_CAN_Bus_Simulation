import can

from src.common.dbc_codec import DBCCodec


def test_speed_message_can_be_decoded():

    codec = DBCCodec()

    payload = codec.encode_speed(65.5)

    message = can.Message(
        arbitration_id=0x100,
        data=payload,
        is_extended_id=False,
    )

    decoded = codec.decode_frame(message)

    assert decoded["VehicleSpeed"] == 65.5
