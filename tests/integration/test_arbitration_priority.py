from src.error_injection.arbitration_test import (
    compare_priority,
)


def test_lower_can_id_has_priority():

    assert (
        compare_priority(0x080, 0x100)
        == 0x080
    )


def test_equal_ids_have_same_priority():

    assert (
        compare_priority(0x100, 0x100)
        == 0x100
    )
