import can
import pytest

from src.common.dbc_codec import DBCCodec


def test_speed_encode_decode_round_trip():

    codec = DBCCodec()

    payload = codec.encode_speed(80.0)

    message = can.Message(
        arbitration_id=0x100,
        data=payload,
        is_extended_id=False,
    )

    decoded = codec.decode_frame(message)

    assert decoded["VehicleSpeed"] == pytest.approx(
        80.0,
        abs=0.01,
    )


def test_speed_rejects_negative_value():

    codec = DBCCodec()

    with pytest.raises(ValueError):
        codec.encode_speed(-1.0)


def test_speed_rejects_out_of_range_value():

    codec = DBCCodec()

    with pytest.raises(ValueError):
        codec.encode_speed(1000.0)
