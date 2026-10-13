from app1 import add


def test_add_positive_numbers():
    assert add(2, 3) == 5


def test_add_negative_numbers():
    assert add(-2, -3) == -5


def test_add_zero():
    assert add(5, 0) == 5


def test_add_decimal_numbers():
    assert add(1.5, 2.5) == 4.0