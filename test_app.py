import pytest

from app import add, subtract


def test_add_basic():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(1.5, 2.5) == 4.0


def test_add_int_and_float():
    assert add(1, 2.5) == pytest.approx(3.5)


def test_subtract_basic():
    assert subtract(5, 2) == 3
    assert subtract(0, 1) == -1
    assert subtract(1.5, 0.5) == pytest.approx(1.0)
